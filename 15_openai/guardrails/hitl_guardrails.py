import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()


@function_tool(needs_approval=True)
async def cancel_order(order_id: int) -> str:
    return f"Cancelled order {order_id}"

agent = Agent(
    name="Support agent",
    instructions="Handle support requests and ask for approval when needed.",
    tools=[cancel_order],
)

async def main() -> None:
    
    # while True:
    #     user_input = input("Enter a support request (or 'exit' to quit): ")
    #     if user_input.lower() == 'exit':
    #         break

    #     result = await Runner.run(agent, user_input)

    #     if result.interruptions:
    #         state = result.to_state()
    #         for interruption in result.interruptions:
    #             user_decision = input(f"Approval needed for: {interruption}. Approve? (y/n): ")
    #             if user_decision.lower() == 'y':
    #                 state.approve(interruption)
    #         result = await Runner.run(agent, state)

    #     print(result.final_output)

    result = await Runner.run(agent, "Cancel order 123.")

    print(f"[Initial Output] {result.raw_responses}")
    if result.interruptions:
        state = result.to_state()
        print("[Interruption] Approval needed for:", result.interruptions)
        for interruption in result.interruptions:
            print(f"Approval needed for: {interruption}. Automatically approving for demo purposes.")
            state.approve(interruption)
        result = await Runner.run(agent, state)

    print(f"[Final Output] {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())