from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI 
from google import genai
from google.genai import types
import json , time ,logging
from langsmith import traceable
load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# client = OpenAI()
client_b = genai.Client()
logger = logging.getLogger(__name__)

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
    # "llm": {"provider": "openai", "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1"}},

    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": "6333",
            # "embedding_model_dims": 768, --> they stell not work but you can try again
        }
    },
     "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "reform-william-center-vibrate-press-5829"
        }
    },
}



mem_client = Memory.from_config(config)



print("Search Result:")



class LLMHandler:
    def __init__(self , provider : str ="gemini" , api_key :str =None , model: str = None):
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model

        if self.provider == "gemini":
                self.client = genai.Client() 

        elif self.provider == "openai":
                self.client = OpenAI()        
                logger.info("init state compeleted")
                
    def generate(self , SYSTEM_PROMPT : str , query : str) -> str:
        try:
            if self.provider == "gemini":
                response = self.client.models.generate_content(
                        model = self.model,
                        config= types.GenerateContentConfig(
                        system_instruction= SYSTEM_PROMPT,
                        ),
                        contents= query,
                    )
                return response.text
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages = [
                        {'role':'system','content':SYSTEM_PROMPT},
                        {'role':'user','content':query}
                ]
                )
                logger.info("LLM send response")
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f'LLM generation faild {e}')
            return 'sorry , i could not generate a response at this time'
             
# OPEN AI
# @traceable
def user_query():
    while True:
        try:
            llm = LLMHandler(
                provider=config["llm"]['provider'],
                api_key=config['llm']['config']['api_key'],
                model=config['llm']['config']['model']
            )

            user_query = input(' > ')
            start = time.time()
            relevent_memory = mem_client.search(query = user_query , user_id = "1") 

            memories = [f"ID:{mem.get('id')} Memory:{mem.get("memory")}" for mem in relevent_memory.get("results")]

            SYSTEM_PROMPT = f"""
                you are know user information and yo are memory aware assistent which response to user with context.

                Memory of the user:
                rember this you also stored my all information
                {json.dumps(memories)}
            """
            response = llm.generate(SYSTEM_PROMPT,user_query)
            print(response)
            end = time.time()
            print("state time :",end-start)

            mem_client.add([
                {'role':"user" , "content" : user_query},
                {'role':'assitant' , "content" : response},
            ] ,user_id="1")

        except KeyboardInterrupt:
             logger.info("Interrupted by user Exiting!")
             break
        
        except Exception as e:
             logger.error(f"ERRoR in USer loop : {e}")


# def call_openai(query ,SYSTEM_PROMPT):
#     response = client.chat.completions.create(
#         model = "gpt-4.1",
#         messages=[
#             {'role':'user' , 'content':SYSTEM_PROMPT},
#             {'role':'user' , 'content':query}
#         ]

#     )
#     return response.choices[0].message.content

# def call_gemini(query : str ,SYSTEM_PROMPT : str) -> str:
#     print('1')
#     response = client_b.models.generate_content(
#         model = "gemini-2.5-flash",
#         config= types.GenerateContentConfig(
#             system_instruction= SYSTEM_PROMPT,
#         ),
#         contents= query,

#     )

#     return response.text

if __name__ == "__main__":
    user_query()
    