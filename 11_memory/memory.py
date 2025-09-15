from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI 
from google import genai
from google.genai import types
import json , time

load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# client = OpenAI()
client_b = genai.Client()


config ={
    "version": "v1.1",

    "embedder":{
        "provider":"gemini",
        "config": {
            'api_key':GEMINI_API_KEY,
            "model":"gemini-embedding-001",
            "output_dimensionality": 1536, 
        },

    },
    "llm": {"provider": "gemini", "config": {"api_key": GEMINI_API_KEY, "model": "gemini-2.0-flash-001"}},
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": "6333",
            # "embedding_model_dims": 768, --> they stell not work but you can try again
        }
    },
}



mem_client = Memory.from_config(config)


# mem_client.add("User like Python and Java but work with Django and FastAPI" , user_id = "raj")

# result = mem_client.search("what freamwork is good for python?", user_id ="raj")
# print(result)
print("Search Result:")
# for data in result['results']:
    # print(data['memory'], "| Score :",data['score'])



# OPEN AI
def user_query():
    while True:
        start = time.time()
        user_query = input(' > ')
        relevent_memory = mem_client.search(query = user_query , user_id = "2") 

        memories = [f"ID:{mem.get('id')} Memory:{mem.get("memory")}" for mem in relevent_memory.get("results")]

        SYSTEM_PROMPT = f"""
            you are know user information and yo are memory aware assistent which response to user with context.

            Memory of the user:
            rember this you also stored my all information
            {json.dumps(memories)}
        """
        # response = call_openai(query , SYSTEM_PROMPT)
        response = call_gemini(user_query , SYSTEM_PROMPT)
        print(response)
        end = time.time()
        print("state time :",end-start)

        mem_client.add([
            {'role':"user" , "content" : user_query},
            {'role':'assitant' , "content" : response},
        ] ,user_id="2")

# def call_openai(query ,SYSTEM_PROMPT):
#     response = client.chat.completions.create(
#         model = "gpt-4.1",
#         messages=[
#             {'role':'user' , 'content':SYSTEM_PROMPT},
#             {'role':'user' , 'content':query}
#         ]

#     )
#     return response.choices[0].message.content

def call_gemini(query,SYSTEM_PROMPT):
    print('1')
    response = client_b.models.generate_content(
        model = "gemini-2.5-flash",
        config= types.GenerateContentConfig(
            system_instruction= SYSTEM_PROMPT,
        ),
        contents= query,

    )

    return response.text

if __name__ == "__main__":
    user_query()
    