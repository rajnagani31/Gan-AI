from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
)
from dotenv import load_dotenv
from agents.decorators import output_guardrail

load_dotenv()


class MessageOutput(BaseModel): 
    response: str

class MathOutput(BaseModel): 
    reasoning: str
    is_math: bool

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="""
    you are a helpful assistant. Check if the user is asking you to do their math homework. 
    if the use is asking about core math concepts, then you can answer the question. then make is_math = False.
    if the user is asking you to do their math homework, then you should not answer the question. then make is_math = True.
    """,
    output_type=MathOutput,
)
class MathGuardrailOutput(BaseModel):
    output_info: str
    tripwire_triggered: bool
    tripwire_message: str

@output_guardrail
async def math_guardrail(  
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
        # tripwire_message=result.final_output.reasoning
    )

agent = Agent( 
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail],
    output_type=MessageOutput,
)

async def main():
    # This should trip the guardrail
    try:
        response = await Runner.run(agent, "Hello")
        print("[Response]", response.final_output.response)
        print("[Guardrail Result]", response.output_guardrail_results[0])
        # print("[Input Tokens]", response)

    except OutputGuardrailTripwireTriggered as w:
        print("Math output guardrail tripped", w)

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())