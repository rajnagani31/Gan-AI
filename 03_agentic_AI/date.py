from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import os
load_dotenv()
client = OpenAI()

# few-shot Prompting: The model is given sum exmple and direction
SYSTEM_PROMPT="""
      you are helpfull ai agent

      today date time is f"{{datetime.now()}}"
      
      """



response=client.chat.completions.create(
    model= "gpt-4.1",
    messages=[
        {'role':'system','content':SYSTEM_PROMPT},
        {'role':'user','content':'what date and time of today'},
        



    ]
)

print(response.choices[0].message.content)
print(datetime.now())