from agents import Agent, Runner, OutputGuardrailTripwireTriggered
from dotenv import load_dotenv
from pydantic import BaseModel
from agents.decorators import output_guardrail
from agents.tool import function_tool




load_dotenv()

class SQLAgentOutput(BaseModel):
    sql_query: str | None = None
    # result: str | None = None

class SQLGuardrailOutput(BaseModel):
    # output_info: str
    tripwire_triggered: bool
    reason : str | None = None




sql_guardrail_agent = Agent(
    name="SQL Guardrail check",
    instructions="""
    Chceck if query is safe to execute. The query should be read only and 
    do not modify, delete and drop any data or tables.
    """,
    output_type=SQLGuardrailOutput
)

@output_guardrail
async def sql_guardrail(ctx: dict, agent: Agent, output: SQLAgentOutput) -> SQLGuardrailOutput:
    print("SQL Guardrail check for query:", output.sql_query)
    result = await Runner.run(sql_guardrail_agent, output.sql_query)
    print("SQL Guardrail Result:", result.final_output)
    print("SQL Guardrail Tripwire Triggered:", result.final_output.tripwire_triggered)
    print("SQL Guardrail Reason:", result.final_output.reason)
    response_data = SQLGuardrailOutput(
        tripwire_triggered=result.final_output.tripwire_triggered,
        reason=result.final_output.reason
    )

    print("gard_result:", response_data)

    return response_data

sql_agent = Agent(
    model="gpt-4o",
    name="SQL Agent",
    instructions="""
    You are a helpful assistant that can answer questions about a database. You have access to the following tools:

    Dummy schema:
    - users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        created_at DATETIME,
        country TEXT
      )
    - comments (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        post_id INTEGER,
        comment TEXT,
        created_at DATETIME,
        likes INTEGER
      )

    Use this schema when answering SQL questions.
    """,
    output_type=SQLAgentOutput,
    output_guardrails=[sql_guardrail],
)

async def main():
    try:
        question = "Drop all user data from users table"
        response = await Runner.run(sql_agent, question)
        print("[Response]", response.final_output.sql_query)
        print("[Full Result]", response)
        print("[Guardrail Results]", response.output_guardrail_results)
    
    except OutputGuardrailTripwireTriggered as e:
        print("Exception:", e)
        print("Attributes:", vars(e))

        gard_result = e.guardrail_result
        print("[Guardrail Result]", gard_result)
        print("[Tripwire Triggered]", gard_result.output.tripwire_triggered)
        print("[Reason]", gard_result.output.reason)

    except Exception as e:
        print("Error:", e)
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
