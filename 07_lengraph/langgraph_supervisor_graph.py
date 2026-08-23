from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

load_dotenv()  # Load environment variables from .env file

model = ChatOpenAI(model="gpt-4o")

# Create specialized agents

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def web_search(query: str) -> str:
    """Search the web for information."""
    return (
        "Here are the headcounts for each of the FAANG companies in 2024:\n"
        "1. **Facebook (Meta)**: 67,317 employees.\n"
        "2. **Apple**: 164,000 employees.\n"
        "3. **Amazon**: 1,551,000 employees.\n"
        "4. **Netflix**: 14,000 employees.\n"
        "5. **Google (Alphabet)**: 181,269 employees."
    )

math_agent = create_react_agent(
    model=model,
    tools=[add, multiply],
    name="math_expert",
    prompt="You are a math expert. Always use one tool at a time."
)

research_agent = create_react_agent(
    model=model,
    tools=[web_search],
    name="research_expert",
    prompt="You are a world class researcher with access to web search. Do not do any math."
)

# Create supervisor workflow
workflow = create_supervisor([research_agent, math_agent], model=model,prompt=("You are a team supervisor managing a research expert and a math expert.,For current events, use research_agent.,For math problems, use math_agent."))

# Compile and run
app = workflow.compile()
result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": "hi"
        }
    ]
})

# print("\n\nFinal Result:", result["messages"][-1].content)

for msg in result["messages"]:
    if hasattr(msg, "usage_metadata") and msg.usage_metadata:
        print("=" * 50)
        print("Agent:", getattr(msg, "name", "Unknown"))
        print("Response:", msg.content)
        print("Tokens:", msg.usage_metadata)

messages = result["messages"]
usage = messages[-1].usage_metadata
print("\nToken Usage")
print(f"Input Tokens : {usage['input_tokens']}")
print(f"Output Tokens: {usage['output_tokens']}")
print(f"Total Tokens : {usage['total_tokens']}")