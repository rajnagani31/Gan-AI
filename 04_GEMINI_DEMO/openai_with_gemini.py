from dotenv import load_dotenv
from openai import OpenAI

import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="""
    you are a helf full ai agent,you know only python programing language
    
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash-preview-05-20",
   
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "hi"
        }
    ]
)

print(response.choices[0].message.content)