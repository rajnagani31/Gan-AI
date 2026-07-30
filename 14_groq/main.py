import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What is fastapi?",
        }
    ],
    model="llama-3.3-70b-versatile",
    stream= True
)

print(chat_completion.choices[0].message.content)
print(chat_completion.choices[0].message.content)
print(chat_completion.choices[0].message.content)
print(chat_completion.choices[0].message.content)
print(chat_completion.choices[0].message.content)

for chunk in chat_completion:
    print(chunk.choices[0].delta.content, end ="")
    print(chunk.choices[0].delta.content, end ="")
    print(chunk.choices[0].delta.content, end ="")
    print(chunk.choices[0].delta.content, end ="")
    print(chunk.choices[0].delta.content, end ="")
    print(chunk.choices[0].delta.content, end ="")
    print(chunk.choices[0].delta.content, end ="")
    print(chunk.choices[0].delta.content, end ="")
    print(chunk.choices[0].delta.content, end ="")
    print(chunk.choices[0].delta.content, end ="")

