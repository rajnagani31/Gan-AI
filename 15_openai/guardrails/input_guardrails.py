from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
)
from dotenv import load_dotenv
from agents.decorators import input_guardrail
from agents.tool import function_tool

load_dotenv()


@function_tool
def two_sum(a: int, b: int) -> int:
    return a + b


class MathHomeworkOutput(BaseModel):
    reason: str
    tripwire_triggered: bool
    input_tokens: int | None = None
    output_tokens: int | None = None


class MathOutput(BaseModel):
    is_math_question: bool = False
    reason: str = ""

guardrail_agent = Agent(
    name="Math Guardrail check",
    model="gpt-4o",
    instructions="""
        You are a guardrail agent. Your ONLY job is to check whether the user's query is a math question.

    Return a JSON-like object with:
    - is_math_question: true or false
    - reason: a short explanation string, always include one

    Rules:
    - If the query is primarily a math question, set is_math_question to true.
    - If it is not primarily a math question, set is_math_question to false and give a short reason.
    - Do NOT treat a query as math just because it contains numbers or mathematical words.

    Examples:
    - "Solve 2x + 5 = 15" → math
    - "What is 25% of 80?" → math
    - "Write a poem about numbers" → not math
    - "Write Python code to add two numbers" → not math
    - "Translate this equation into French" → not math
    """,
    output_type=MathOutput,
)


@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    output = result.final_output

    for response in result.raw_responses:
        if response.usage:
            total_input = response.usage.input_tokens
            total_output = response.usage.output_tokens
            total_tokens = response.usage.total_tokens
            print("[Gardrail Usage] Input tokens:", total_input)
            print("[Gardrail Usage] Output tokens:", total_output)
            print("[Gardrail Usage] Total tokens:", total_tokens)

    is_math_question = bool(output.is_math_question)
    tripwire_triggered = not is_math_question
    reason = (output.reason or "").strip() or (
        "This is a math question." if is_math_question else "This is not primarily a math question."
    )

    custom_response = MathHomeworkOutput(
        reason=reason,
        tripwire_triggered=tripwire_triggered,
        input_tokens=total_input,
        output_tokens=total_output,
    )

    return GuardrailFunctionOutput(
        output_info=custom_response,
        tripwire_triggered=tripwire_triggered,
    )

agent = Agent(  
    name="Math agent",
    model="gpt-4o",
    instructions="You are a math agent. You help users solve math problems.",
    tools=[two_sum],
    input_guardrails=[math_guardrail],
)

# query ="Hello, can you help to addition of two numbers: x = 5 and y = 10? so that I can get the sum of x and y and solve this question : x - 2y = 5"
query = 'hi'
# query = 'give me two sum code in js'
# query = 'write a poem about the sun and the moon'

async def main():
    # This should trip the guardrail
    try:
        result = await Runner.run(agent, query)
        print("[Response]", result.final_output,'\n')
        print("[New Items]", result.new_items,'\n')
        print("[Raw Responses]", result.raw_responses,'\n')
        print("[Guardrail Result]", result.input_guardrail_results,'\n')
        # print
        print("[full result]", result,'\n')
        print("Guardrail didn't trip - this is unexpected")
        total_input = 0
        total_output = 0
        total_tokens = 0

        for response in result.raw_responses:
            if response.usage:
                total_input += response.usage.input_tokens
                total_output += response.usage.output_tokens
                total_tokens += response.usage.total_tokens

        print("Input tokens:", total_input)
        print("Output tokens:", total_output)
        print("Total tokens:", total_tokens)

    except InputGuardrailTripwireTriggered as e:
        print("Guardrail tripwire triggered - this is expected")
        print("[Response]", e)
        print("Attributes:", vars(e))
        print("[Guardrail Result]", e.guardrail_result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())