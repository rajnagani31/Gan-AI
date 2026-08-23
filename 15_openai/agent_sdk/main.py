import asyncio

from agents import Agent, Runner
from dotenv import load_dotenv


load_dotenv()

agent = Agent(
    name="History tutor",
    instructions="You answer history questions clearly and concisely.",
    model="gpt-5.6",
)


async def main() -> None:
    """
    result sent this pyload:

    - Last agent: Agent(name="History tutor", ...)
    - Final output (str):
        The Western Roman Empire traditionally fell in **476 CE**, when the last western emperor, Romulus Augustulus, was deposed.
        
        The Eastern Roman (Byzantine) Empire continued until **1453**, when Constantinople fell to the Ottoman Empire.
    - 1 new item(s)
    - 1 raw response(s)
    - 0 input guardrail result(s)
    - 0 output guardrail result(s)
    (See `RunResult` for more details)
    """
    result = await Runner.run(agent, "Ho")
    print(result.final_output)
    print("[Full Result]", result)
    # print(result.new_items)


if __name__ == "__main__":
    asyncio.run(main())