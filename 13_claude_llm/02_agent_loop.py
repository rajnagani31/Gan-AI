import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions,AssistantMessage, ResultMessage
from click import option

prompt = """wat is my name?"""
options= ClaudeAgentOptions(
    # allowed_tools=["get_weather","run_command"],
    permission_mode = "acceptEdits",
)
async def main():
    
    async for message in query(
        prompt=prompt,
        options=options
        ):

        print(message)
        # if isinstance(message,AssistantMessage):
        #     for block in message.content:
        #         if hasattr(block,"text"):
        #             print(block.text)
        #         elif hasattr(block,"name"):
        #             print(f"Tool: {block.name}")
        # elif isinstance(message, ResultMessage):
        #     print(f"Done: {message.subtype}")

asyncio.run(main())
