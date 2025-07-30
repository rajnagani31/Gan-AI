from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from google import genai
from dotenv import load_dotenv
from google.genai.types import GenerateContentConfig
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
client= genai.Client()

class State(TypedDict):
    query: str
    llm_result: str | None

class Mygraph:    
    def __init__(self,state :State):
        pass

    def chat_bot(self , state :State):
        query=state['query']
        response= client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query,
            config=GenerateContentConfig(system_instruction=["you onley give answer on coding query any other not"]),

        )
        # result = response.text
        # state["llm_result"]=result
        state['llm_result'] = getattr(response,"text",  str(response))
        return state

    def graph_builder(self,query):
        graph_builder= StateGraph(State)

        graph_builder.add_node("chat_bot",self.chat_bot)

        # edges

        graph_builder.add_edge(START,"chat_bot"),
        graph_builder.add_edge("chat_bot",END)

        graph=graph_builder.compile()
        
        _state: State ={
            "query":query,
            "llm_result": None
        }
        response=graph.invoke( _state )
        return response
    

query='what is my last query'
my_graph = Mygraph(None)

result= my_graph.graph_builder(query)
print(result)