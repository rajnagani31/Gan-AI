from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from dotenv import load_dotenv
import requests
from google import genai

load_dotenv()
client_gemini=genai.Client()

@tool()
def two_number_add(a :int ,b :int):
    """ This tool add two numbers"""
    return a+b

@tool()
def get_weather(city : str):
    """ this tool return the weather data about the given city """
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return f"Somthing what wrong"

@tool()
def coding_tool(query : str):
    """ 
    this tool return write coding answer in any type of qestion
    
    
    """
    return query

def add_three_number(a ,b,c : int):
    """ you are add there number"""
    return a + b+c

todos=[]
@tool()
def add_todo(task :str):
    """ you are add todo in todos"""
    todos.append(task)
    return task


@tool()
def get_todo():
    """ you are get todo list to user"""
    return todos

@tool()
def generel_(query :str):
    """ you give answer only generel query hi,hello etc"""
    print("⚠️ start generel")

    query=query
    print('h1')
    response=client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        
        
    )
    return response.text

tools=[get_weather,two_number_add,coding_tool,add_three_number,add_todo,get_todo,generel_]
class State(TypedDict):
    messages:Annotated[list,add_messages]

llm= init_chat_model( model_provider="openai",model="gpt-4.1-nano",)
llm_with_tool=llm.bind_tools(tools)


def chat_bot(state: State):
    message=llm_with_tool.invoke(state['messages'])
    return {"messages":[message]}

tool_node=ToolNode(tools=tools)
graph_builder=StateGraph(State)

graph_builder.add_node("chat_bot",chat_bot)
graph_builder.add_node("tools",tool_node)

graph_builder.add_edge(START,"chat_bot")
graph_builder.add_conditional_edges(
    "chat_bot",
    tools_condition,
)
graph_builder.add_edge('tools','chat_bot')
# graph_builder.add_edge("chat_bot",END)

graph=graph_builder.compile()

def main():
    while True:
        query=input("> ")
        state= State(
            messages=[{'role':'user','content':query}]
        )


        for event in graph.stream(state,stream_mode='values'):
            if "messages" in event:
                event["messages"][-1].pretty_print()

        # result=graph.invoke(state)
        # print(result)
main()    