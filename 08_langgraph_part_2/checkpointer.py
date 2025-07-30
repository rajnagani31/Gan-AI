from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
from google import genai
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()
# client=genai.Client()

print('1')


class State(TypedDict):
    messages:Annotated[list,add_messages]
    print('2')


llm= init_chat_model( model_provider="openai",model="gpt-4.1",)
# llm= init_chat_model( model_provider="google_genai",model="gpt-4.1",)

def compile_graph_with_checkpinter(checkpointer):
    graph_with_checkpointer=graph_builder.compile(checkpointer=checkpointer)
    print('3')

    return graph_with_checkpointer


def chat_node(state:State):
    print('a')

    response=llm.invoke(state['messages'])
    print('b')

    print('4')
    print('c')
    return {'messages':[response]}

print('d')
graph_builder=StateGraph(State)

graph_builder.add_node("chat_node",chat_node)

graph_builder.add_edge(START,"chat_node")
graph_builder.add_edge("chat_node",END)

graph=graph_builder.compile()

def main():
    print('e')
    DB_URL="mongodb://admin:admin@localhost:27017" 
    print('d')
    config={"configurable":{"thread_id":1}}
    print('k')
    with MongoDBSaver.from_conn_string(DB_URL) as mongo_check_pointer:
        print('j')
        query=input(">>")
        print("call")
        graph_with_mongo=compile_graph_with_checkpinter(mongo_check_pointer)
        print('call end')
        result=graph_with_mongo.invoke({'messages': [{"role": "assistant", "content": query}]},config) # is work
        print('result')
        # result=graph_with_mongo.invoke({'messages':query},config) # is both work ok
        print(result)
    
main()    