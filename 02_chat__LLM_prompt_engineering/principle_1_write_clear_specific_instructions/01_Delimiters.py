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
        ],
        temperature=0,
        # top_p=1
    )
    return response.choices[0].message.content


# Tactic 1: Use delimiters to clearly indicate distinct parts of the input

# This is the content you want the model to summarize.
text = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""

# ``{text}``` Summarize the text and prompt see somthing like prompt + ```above text````
prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""

prompt1 = f"""
give me correcte answer for this math problem: 
problem mentioned in the triple backticks:\

```{2+2}```

"""
response = get_completion(prompt1)
print(response)

