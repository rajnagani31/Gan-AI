import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR.parent / ".env")


def call_groq(user_query: str, system_instruction: str) -> str:
    """Call Groq through the official Groq Python SDK."""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_query},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""
