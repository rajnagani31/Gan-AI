from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

r = client.chat.completions.create(
    model="gpt-4.1",
        messages=[
            {'role':'user' , 'content':'hi'},
        ]

)

print(r.choices[0].message.content)