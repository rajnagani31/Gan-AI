from agents.llm_langchain_groq import run_agent as run_groq_agent
from agents.llm_langchain_openai import run_agent as run_openai_agent


def llm_langchain_openai(user_query: str) -> None:
    """Run the streaming OpenAI LangChain bot."""
    print("\n--- LangChain OpenAI Bot ---")
    run_openai_agent(user_query)


def llm_langchain_groq(user_query: str) -> None:
    """Run the streaming Groq LangChain bot."""
    print("\n--- LangChain Groq Bot ---")
    run_groq_agent(user_query)


if __name__ == "__main__":
    query = "What is on the settings page?"
    query = 'Hi, how are you?'
    query = "What is profile and where is in UI?"

    # Run either one bot or both bots with the same user query.
    llm_langchain_openai(query)
    llm_langchain_groq(query)
