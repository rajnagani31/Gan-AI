
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

print(response.choices[0].message.content)