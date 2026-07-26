import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq

# Allow this file to run directly from the agents folder.
PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from system_instruction import SYSTEM_PROMPT
from tools import get_product_doc_content, get_product_index, get_weather

load_dotenv(PROJECT_DIR.parent / ".env")

available_tools = [get_weather, get_product_index, get_product_doc_content]
tool_map = {tool.name: tool for tool in available_tools}
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_retries=2)
llm_with_tools = llm.bind_tools(available_tools)


def stream_response(messages: list) -> AIMessage:
    """Print one streamed Groq turn and preserve requested tool calls."""
    chunks = []
    for chunk in llm_with_tools.stream(messages):
        chunks.append(chunk)
        if chunk.content:
            print(chunk.content, end="", flush=True)

    merged = chunks[0]
    for chunk in chunks[1:]:
        merged += chunk
    return AIMessage(content=merged.content or "", tool_calls=merged.tool_calls)


def run_agent(user_message: str) -> None:
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_message)]

    # Continue through index -> document -> final answer, or other tool sequences.
    for _ in range(6):
        ai_message = stream_response(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            print()
            return

        for tool_call in ai_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            print(f"\n[Executing tool: {tool_name} with args: {tool_args}]")
            tool_result = tool_map[tool_name].invoke(tool_args)
            print(f"Tool result: {tool_result}\n")

            # This ToolMessage sends the tool result back to the LLM.
            messages.append(ToolMessage(
                content=str(tool_result),
                name=tool_name,
                tool_call_id=tool_id,
            ))

    print("\nStopped after six tool rounds to prevent an infinite tool loop.")


if __name__ == "__main__":
    run_agent("What is on the settings page?")
