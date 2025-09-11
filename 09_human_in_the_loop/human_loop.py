import requests
from langchain.chat_models import init_chat_model
from typing import List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END  
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import  ToolNode , tools_condition
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.types import interrupt, Command




load_dotenv()

class State(TypedDict):
    messages : Annotated[list,add_messages]

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt(
        {"query": query})  # This saves the state in DB and kills the graph
    return human_response["data"]

@tool()
def get_weather(city : str):
    """ this tool return the weather data about the given city """
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return f"Somthing what wrong"


tools=[get_weather,human_assistance]
llm= init_chat_model("openai:gpt-4.1")
# llm = init_chat_model(model_provider="openai", model="gpt-4.1")
llm_with_tool = llm.bind_tools(tools)

def chat_bot(state : State):
    message = llm_with_tool.invoke(state["messages"])
    return {"messages":[message]}

tool_node = ToolNode(tools=tools)
graph = StateGraph(State)


graph.add_node("chat_bot",chat_bot)
graph.add_node("tools",tool_node)

graph.add_edge(START,"chat_bot")
graph.add_conditional_edges(
    "chat_bot",
    tools_condition
)
graph.add_edge("tools","chat_bot") # NOTE --> This node will work parallel multiple times for USA ,Surat,rajkot ,ETC
graph.add_edge("chat_bot",END)

# start_graph=graph.compile()

def creat_graph(cheakpointer):
    return graph.compile(checkpointer=cheakpointer)

def main():
    DB_URL = "mongodb://admin:admin@localhost:27017/"
    config ={ "configurable" :  { "thread_id" : 51}}

    while True:
        with MongoDBSaver.from_conn_string(DB_URL) as mongo_cheakpointer:
            graph_with_mongo = creat_graph(mongo_cheakpointer)
            query = input(">>")

            state = State(
                messages = [{"role":"user","content" : query}]
            )
            # state : State = {"messages":[{"role":"user","content":query}]}
            # result = start_graph.stream(state , stream_mode="values")

            for ans in graph_with_mongo.stream(state,config,stream_mode="values"):
                if "messages" in ans:
                    ans['messages'][-1].pretty_print()

import json
def admin_call():
        DB_URL = "mongodb://admin:admin@localhost:27017/"
        config ={ "configurable" :  { "thread_id" : 51}}

        with MongoDBSaver.from_conn_string(DB_URL) as mongo_cheakpointer:
            graph_with_mongo = creat_graph(mongo_cheakpointer)

            state = graph_with_mongo.get_state(config=config)
            last_message = state.values['messages'][-1]
            tool_calls = last_message.additional_kwargs.get("tool_calls", [])
            user_query = None

            for call in tool_calls:
                if call.get("function", {}).get("name") == "human_assistance":
                    args = call["function"].get("arguments", "{}")
                    try:
                        args_dict = json.loads(args)
                        user_query = args_dict.get("query")
                    except json.JSONDecodeError:
                        print("Failed to decode function arguments.")

            print("User Has a Query", user_query)
            solution = input("> ")

            resume_command = Command(resume={"data": solution})

            for event in graph_with_mongo.stream(resume_command, config, stream_mode="values"):
                if "messages" in event:
                    event["messages"][-1].pretty_print()


    
if __name__ == "__main__":
    main()
    
# admin_call()    
