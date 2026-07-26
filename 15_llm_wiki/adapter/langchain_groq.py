# import os
# from collections.abc import Iterator
# from typing import Any

# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_groq import ChatGroq

# from .base import BaseLLMAdapter


# class LangChainGroqAdapter(BaseLLMAdapter):
#     """Groq chat adapter implemented with LangChain."""

#     def __init__(
#         self,
#         model: str = "llama-3.1-8b-instant",
#         temperature: float = 0.2,
#     ) -> None:
#         super().__init__()
#         self.chat = ChatGroq(
#             model=model,
#             temperature=temperature,
#             api_key=os.environ.get("GROQ_API_KEY"),
#         )

#     def invoke(self, prompt: str, system_instruction: str | None = None, tools: list[dict[str, Any]] | None = None) -> str:
#         chat = self._configured_chat(tools)
#         response = chat.invoke(self._messages(prompt, system_instruction))
#         self.last_tool_calls = response.tool_calls or []
#         return self._content_to_text(response.content)

#     def stream(self, prompt: str, system_instruction: str | None = None, tools: list[dict[str, Any]] | None = None) -> Iterator[str]:
#         self.last_tool_calls = []
#         chat = self._configured_chat(tools)
#         for chunk in chat.stream(self._messages(prompt, system_instruction)):
#             if chunk.tool_calls:
#                 self.last_tool_calls = chunk.tool_calls
#             text = self._content_to_text(chunk.content)
#             if text:
#                 yield text

#     def _configured_chat(self, tools: list[dict[str, Any]] | None) -> Any:
#         attached_tools = self.tools if tools is None else tools
#         return self.chat.bind_tools(attached_tools) if attached_tools else self.chat

#     def _messages(self, prompt: str, instruction: str | None) -> list[Any]:
#         active_instruction = self.system_instruction if instruction is None else instruction
#         messages: list[Any] = [HumanMessage(content=prompt)]
#         if active_instruction:
#             messages.insert(0, SystemMessage(content=active_instruction))
#         return messages

#     @staticmethod
#     def _content_to_text(content: object) -> str:
#         if isinstance(content, str):
#             return content
#         if isinstance(content, list):
#             return "".join(
#                 item.get("text", "") if isinstance(item, dict) else str(item)
#                 for item in content
#             )
#         return str(content or "")
