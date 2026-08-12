import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from agents.llm_groq import call_groq
from agents.llm_openai import call_openai
from system_instruction import SYSTEM_PROMPT

load_dotenv()


def llm_openai(user_query: str) -> str:
    """Call the OpenAI SDK implementation."""
    return call_openai(user_query, SYSTEM_PROMPT)


def llm_groq(user_query: str) -> str:
    """Call the Groq SDK implementation."""
    return call_groq(user_query, SYSTEM_PROMPT)


def llm_langchain_openai(user_query: str) -> str:
    """Call OpenAI through LangChain."""
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        api_key=os.environ.get("OPENAI_API_KEY"),
        temperature=0,
        max_completion_tokens=24,
        max_retries=2,
    )
    response = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", user_query),
    ])
    return str(response.content)


def llm_langchain_groq(user_query: str) -> str:
    """Call Groq through LangChain."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.environ.get("GROQ_API_KEY"),
        temperature=0,
        max_retries=2,
        # max_completion_tokens=240
    )
    response = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", user_query),
    ])
    return str(response.content)


if __name__ == "__main__":
    query = "What is artificial intelligence?"
    providers = {
        # "OpenAI SDK": llm_openai,
        # "Groq SDK": llm_groq,
        # "LangChain OpenAI": llm_langchain_openai,
        "LangChain Groq": llm_langchain_groq,
    }

    print(f"User query: {query}\n")
    for name, llm_function in providers.items():
        print(f"{name} response:")
        print(llm_function(query))
        print()
