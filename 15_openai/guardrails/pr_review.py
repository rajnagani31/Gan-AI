from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
)
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from agents.decorators import input_guardrail
from agents.tool import function_tool
import asyncio
load_dotenv()


@function_tool
def two_sum(a: int, b: int) -> int:
    return a + b


class PRReviewOutput(BaseModel):
    is_pr_review_request: bool = False
    reason: str = ""

pr_review= Agent(
    name="PR Review Guardrail check",
    model="gpt-4o",
    instructions="""
        You are a guardrail agent. Your ONLY job is to check whether the user's query is a PR review request.
        """,

    output_type=PRReviewOutput,
)

@input_guardrail(run_in_parallel=False)
async def pr_review_guardrail(
    ctx: RunContextWrapper, agent: Agent, input_items: list[TResponseInputItem]
):
    print("[context]", ctx)
    agent_result = await Runner.run(pr_review, input_items, context=ctx.context)
    output = agent_result.final_output

    is_pr_review_request = bool(output.is_pr_review_request)
    tripwire_triggered = not is_pr_review_request
    tripwire_message = output.reason

    for response in agent_result.raw_responses:
        if response.usage:
            total_input = response.usage.input_tokens
            total_output = response.usage.output_tokens
            total_tokens = response.usage.total_tokens
            print("[Gardrail Usage] Input tokens:", total_input)
            print("[Gardrail Usage] Output tokens:", total_output)
            print("[Gardrail Usage] Total tokens:", total_tokens)

    return GuardrailFunctionOutput(
        output_info=output.dict(),
        tripwire_triggered=tripwire_triggered
    )

pr_review_agent = Agent(
    name="PR Review Agent",
    model="gpt-4o",
    instructions="""
        You are PR review agent.

        your job is to review the pr code and and check logic and variables are correct and if there are any errors in the code.

        then tell the user about code, errors and logic issues etc..
    """,
    # output_type=PRReviewOutput,
    input_guardrails=[pr_review_guardrail],
)

query ="""
    -def add(a, b):
    +def add(a, b) -> int:
        return a + c
    review this pr code and make sure it is correct    
"""
query = 'hi'
async def main():
    # This should trip the guardrail
    try:
        response = await Runner.run(pr_review_agent, query)
        # response  = Runner.run_streamed(pr_review_agent, "Please review my PR for the new feature")
        # async for event in response.stream_events():
            # print("Event:", event)
            # if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                # print(event.data.delta, end="", flush=True)
                # if event.data.delta:
                #     if "reason" in event.data.delta:
                #         print(event.data.delta, end="", flush=True)
                # print(event)
        print("[Response]", response)
    except InputGuardrailTripwireTriggered as e:
        print("[Guardrail Tripwire Triggered]", e)
        print("[Attributes]", vars(e))
        print("[Guardrail Result]", e.guardrail_result)

if __name__ == "__main__":
    asyncio.run(main())