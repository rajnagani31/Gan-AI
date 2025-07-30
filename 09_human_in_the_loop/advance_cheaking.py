from google import genai 
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated,Literal
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.tools import tool
from pydantic import BaseModel
from openai import OpenAI
from langgraph.graph import StateGraph,START,END
from langchain.chat_models import init_chat_model
import os,requests


load_dotenv()
client=OpenAI()
client_gemini=genai.Client()
client_a=OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),

    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
class ClassifyMessageResponse(BaseModel):
    is_generel_qestion: bool


class State(TypedDict):
    messages:Annotated[list,add_messages]
    # messages:str

    # llm_result:str
    is_generel_qestion: bool | None

def cheaking(state : State):
    result_cheak=state["is_generel_qestion"]
    print(result_cheak)



# cheaking

def classify_messages(state :State):
    print("⚠️ cheakin start")
    print('1')
    query=state['messages']
    print(query)
    print('2')


    SYSTEM_PROMPT="""
                you give only boolian valiu True and False
                
                user ask hi,hello,how are you and any other normal qestion you retur True
                &
                while user ask any other type of qestion you return False 
                """
    response=client_a.beta.chat.completions.parse(
        model="gemini-1.5-flash",
        # model="gpt-4.1-nano",
        response_format=ClassifyMessageResponse,

        messages=[
            {'role':'system','content':SYSTEM_PROMPT},
            {'role':'user','content': query}
        ]
    )
    is_generel_qestion_=response.choices[0].message.parsed.is_generel_qestion
    state['is_generel_qestion']=is_generel_qestion_
    cheaking(state)

    return state
    


# rout query
def rout_query(state:State)->Literal['Hi_hello',"chat_bot"]:
    print("⚠️ routing start")
    
    is_generel=state['is_generel_qestion']
    if is_generel:
        return "Hi_hello"
    return "chat_bot"


# hi hello node

def Hi_hello(state :State):
    print("⚠️ start generel")

    query=state['messages']

    response=client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        
        
    )
    result=response.text
    state['llm_result']=result

    return state



# ------->tool
@tool()
def coding(query :str) :
    """ 
    this tool return write coding answer in any type of qestion
    
    
    """
    return query

@tool()
def get_weather(city : str):
    """ this tool return the weather data about the given city """
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return f"Somthing what wrong"


# Todo section

@tool()
def add_task(task :str):
    """ You add task """
    
    with open("todos.txt","w") as file:
        file.write(str(task))
    return task

@tool()
def get_task():
    """ you give task list to user and task return in string formet"""
    with open("todos.txt",'r') as file:
        return file.read()
# startin tools part
tools=[coding,get_weather,add_task,get_task]



llm=init_chat_model(model_provider="openai",model="gpt-4.1-nano")
llm_with_tool=llm.bind_tools(tools)

def chat_bot(state:State):
    print("⚠️ start chat bot")

    message=llm_with_tool.invoke(state['messages'])
    print('1')
    # state['llm_result']=message
    return {"messages":[message]}

    # return state
    


# Use instantiated objects.
tool_node=ToolNode(tools=tools)
graph_builder=StateGraph(State)

graph_builder.add_node("classify_messages",classify_messages)
graph_builder.add_node("rout_query",rout_query)
graph_builder.add_node("Hi_hello",Hi_hello)
graph_builder.add_node("chat_bot",chat_bot)
graph_builder.add_node('tools',tool_node)


# edges

# graph_builder.add_edge(START,"classify_messages")
# graph_builder.add_conditional_edges("classify_messages",rout_query)
# graph_builder.add_edge("Hi_hello",END)
# graph_builder.add_edge("chat_bot",END)
graph_builder.add_edge(START,"chat_bot")
graph_builder.add_conditional_edges(
    "chat_bot",
    tools_condition,
)
graph_builder.add_edge('tools','chat_bot')


graph=graph_builder.compile()

def main():
    while True:
        query=input(">>")

        _state: State= {
            "messages":query,
            "llm_result":None,
            'is_generel_qestion':False
        }
        state=State(
            {"messages":[{'role':'user','content':query}],}   
            
        )

        for event in graph.stream(state,stream_mode='values'):
                if 'messages' in event:
                    event['messages'][-1].pretty_print()
        # response=graph.invoke(_state)
        # print(response['llm_result'])
        
        # r=chat_bot(state)
        # print(r)
main()
