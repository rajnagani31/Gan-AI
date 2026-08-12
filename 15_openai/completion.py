from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-5.6",
    messages=[
        {
            "role": "user",
            "content": "hi",
        }
    ],
)

print(completion.choices[0].message.content)

print(completion)