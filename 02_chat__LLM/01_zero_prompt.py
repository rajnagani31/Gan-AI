
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# zero-shot Prompting: The model is given a direct question or task
SYSTEM_PROMPT="""
        you are an export in python.you only know about python and nothing else.
        you help user in solveing python doubts and nothin else.
        user ask any other type of qestion ,you give remminder of python not other in  Angry emotion.

        Example:
        user:Indian stock market data
        Assistant:yes know about stock market  
"""


response=client.chat.completions.create(
    model= "gpt-4.1-mini",
    messages=[
        {'role':'system','content':SYSTEM_PROMPT},
        {'role':'user','content':'my name is raj'},

        {'role':'assistant','content':'Hello Raj! How can I assist you today?'},
        {'role':'user','content':'give syntext of prime number find'},
        {'role':'user','content':'indian stock market?'},



        

        

    ]
)

print(response.choices[0].message.content)