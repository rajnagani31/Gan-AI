
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# few-shot Prompting: The model is given sum exmple and direction
SYSTEM_PROMPT="""
        you are an export in python.you only know about python and nothing else.
        you help user in solveing python doubts and nothin else.
        If user tried to ask something else apart from Python you can just roast them.


        Example:
        user:zomato today share price?
        Assistant:yes i find Zomato share price.

        Example:
        User:How to make chai?
        Assistant:yes i am Expart in chia and coffe.  
"""


response=client.chat.completions.create(
    model= "gpt-4.1-mini",
    messages=[
        {'role':'system','content':SYSTEM_PROMPT},
        {'role':'user','content':'zomato today share price'},
        {'role':'user','content':'write zomato today share price in python code?'},
        {'role':'user','content':'give method for make chai'},
        {'role':'user','content':'you know about today zomato share price'},



    ]
)

# print(response.choices[0].message.content)


from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()   

def get_completion(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

prompt = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""
response = get_completion(prompt)
print(response)