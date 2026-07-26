import os
from collections.abc import Iterator
from typing import Any

from groq import Groq

from .base import BaseLLMAdapter


class GroqAdapter(BaseLLMAdapter):
    """Groq chat adapter implemented directly with the Groq Python SDK."""

    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.2,
    ) -> None:
        super().__init__()
        self.model = model
        self.temperature = temperature
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def invoke(self, prompt: str, system_instruction: str | None = None, tools: list[dict[str, Any]] | None = None) -> str:
        response = self.client.chat.completions.create(**self._request(prompt, system_instruction, tools))
        self.last_tool_calls = [call.model_dump() for call in response.choices[0].message.tool_calls or []]
        return response.choices[0].message.content or ""

    def stream(self, prompt: str, system_instruction: str | None = None, tools: list[dict[str, Any]] | None = None) -> Iterator[str]:
        self.last_tool_calls = []
        request = self._request(prompt, system_instruction, tools)
        response = self.client.chat.completions.create(**request, stream=True)
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.tool_calls:
                self.last_tool_calls.extend(call.model_dump() for call in delta.tool_calls)
            if delta.content:
                yield delta.content

    def _request(self, prompt: str, instruction: str | None, tools: list[dict[str, Any]] | None) -> dict[str, Any]:
        active_instruction = self.system_instruction if instruction is None else instruction
        messages: list[dict[str, str]] = [{"role": "user", "content": prompt}]
        if active_instruction:
            messages.insert(0, {"role": "system", "content": active_instruction})
        request: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        attached_tools = self.tools if tools is None else tools
        if attached_tools:
            request["tools"] = attached_tools
        return request
