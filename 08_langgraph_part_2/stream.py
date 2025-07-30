from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from typing import Literal
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
import os
from openai import OpenAI
from google.genai.types import GenerateContentConfig, HttpOptions

load_dotenv()

# openai sdk
client_a=OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),

    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# gemini
client=genai.Client()

class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool

class CodeAccuracyResponse(BaseModel):
    accuracy_percentage: str

class State(TypedDict):

    query:str
    llm_result: str | None
    accuracy_percentage:str | None
    Is_codeing_qestion : bool | None



def classify_messages(state : State):
    print("⚠️ classify start")
    query=state['query']

    SYSTEM_PROMPT="""

"""

    response=client_a.beta.chat.completions.parse(
        model="gemini-1.5-flash",
        response_format=ClassifyMessageResponse,
        messages=[
            {'role':'system','content':SYSTEM_PROMPT},
            {'role':"user",'content':query}
        ]
    )
    is_coding_question=response.choices[0].message.parsed.is_coding_question
    state['Is_codeing_qestion'] = is_coding_question

    return state

 

def rout_query(state:State) ->Literal["general_query","coding_query"]:
    print("⚠️ routing start")

    is_coding=state["Is_codeing_qestion"]
    if is_coding:
        return "coding_query"
    return "general_query"

def general_query(state:State):
    print("⚠️ is general")

    query=state['query']

    response=client.models.generate_content(
       model="gemini-2.0-flash",
       contents=query,
       config=GenerateContentConfig(system_instruction=[""]),
    )

    result=response.text
    # print(result)
    state["llm_result"]=result
    
    return state


def coding_query(state:State):
    print("⚠️ is coding")

    query=state['query']

    response=client.models.generate_content(
       model="gemini-2.0-flash-lite",
       contents=query,
       config=GenerateContentConfig(system_instruction=[""]),
    )

    result=response.text
    state["llm_result"]=result    
    return state

def codin_validate_query(state:State):
    print("⚠️ code validate")
    
    llm=state['llm_result']
    query=state['query']

    SYSTEM_PROMPT=f"""
        you are an expert in calculatin accuracy of the code according to the question.
        return the persentage of accuracy
        user query:{query}
        code:{llm}
"""

    response=client_a.beta.chat.completions.parse(
        model="gemini-1.5-flash",
        response_format=CodeAccuracyResponse,
        messages=[
            {'role':'system','content':SYSTEM_PROMPT},
            {'role':"user",'content':query}
        ]
    )
    state['accuracy_percentage'] = response.choices[0].message.parsed.accuracy_percentage

    return state
# graph  builder 
graph_builder= StateGraph(State)

# define node

graph_builder.add_node("classify_messages",classify_messages)
graph_builder.add_node("rout_query",rout_query)
graph_builder.add_node("general_query",general_query)
graph_builder.add_node("coding_query",coding_query)
graph_builder.add_node("codin_validate_query",codin_validate_query)


# define edge

graph_builder.add_edge(START,"classify_messages")
graph_builder.add_conditional_edges("classify_messages",rout_query)
graph_builder.add_edge('general_query',END)
graph_builder.add_edge('coding_query',"codin_validate_query")
graph_builder.add_edge('codin_validate_query',END)

graph=graph_builder.compile()

def main():
    print("🧠 start")
    query=input(">>")

    _state: State={
        "query":query,
        "llm_result":None,
        "accuracy_percentage":None,
        "Is_codeing_qestion":False, 
    }

    # response=graph.invoke(_state)

    # print(response)

    for event in graph.stream(_state):
        print(event)

main()          