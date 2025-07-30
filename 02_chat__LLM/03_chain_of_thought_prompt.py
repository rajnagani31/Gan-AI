
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI()

# chain-of-thought Prompting:work step by step in thinl,anylase,result,validate etc..
SYSTEM_PROMPT="""
        You are an helpfull AI assistant who is specialized in resolving user query.
    For the given user input, analyse the input and break down the problem step by step.

    The steps are you get a user input, you analyse, you think, you think again, and think for several times and then return the output with an explanation. 

    Follow this stap in sqeuence that is "analyse","Think","Output","validate" and finally "result"

    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query,

    Output Format:
    {{ "step": "string", "content": "string" }}

    Example:
    Input: What is 2 + 2
    Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operation" }}
    Output: {{ "step": "think", "content": "To perform this addition, I must go from left to right and add all the operands." }}
    Output: {{ "step": "output", "content": "4" }}
    Output: {{ "step": "validate", "content": "Seems like 4 is correct ans for 2 + 2" }}
    Output: {{ "step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers" }}x
"""


# response=client.chat.completions.create(
#     model= "gpt-4.1-mini",
#     messages=[
#         {'role':'system','content':SYSTEM_PROMPT},
#         {'role':'system','content':"what is ans of first 10 even number?"},
#         {'role':'assistant','content':json.dumps({ "step": "analyse", "content": "The user wants the sum of the first 10 even numbers." })},
#         {'role':'assistant','content':json.dumps({"step": "think", "content": "The first 10 even numbers are 2, 4, 6, 8, 10, 12, 14, 16, 18, 20. To find their sum, I will add these numbers together."})},
#         {'role':'assistant','content':json.dumps({"step": "output", "content": "The sum of the first 10 even numbers is 2 + 4 + 6 + 8 + 10 + 12 + 14 + 16 + 18 + 20 = 110."})},
#         {'role':'assistant','content':json.dumps({"step": "validate", "content": "The result 110 is correct because the sum of the first n even numbers is n*(n+1). Here n=10, so 10*11=110."})},
#         {'role':'assistant','content':json.dumps({"step": "result", "content": "The sum of the first 10 even numbers is 110, calculated using the formula n*(n+1) where n=10."})},
        
        


#     ]
# )

# print(response.choices[0].message.content)


messages=[
    {'role':"system" ,"content":SYSTEM_PROMPT}
]

query=input(">> ")
messages.append({'role':'user','content':query})


while True:
    response=client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=messages

    )
    messages.append({"role":"assistant",'content':response.choices[0].message.content})
    parsed_response = json.loads(response.choices[0].message.content)

    if parsed_response.get("step") == "think":
        messages.append({'role':'assistant','content':'<>'})
        continue

    if parsed_response.get("step") != "result":
        print(f"{"       🧠:"},{parsed_response.get('step')},{parsed_response.get("content")}")
        continue

    print(f"{" ✔:"},{parsed_response.get('step')},{parsed_response.get('content')}")
    break

