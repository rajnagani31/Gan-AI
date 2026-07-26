import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR.parent / ".env")


def call_openai(user_query: str, system_instruction: str) -> str:
    """Call OpenAI through the official OpenAI Python SDK."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_query},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""
