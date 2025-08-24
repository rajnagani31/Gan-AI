from langgraph.graph import StateGraph,START,END
from typing import Literal,Annotated
from typing_extensions import TypedDict
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv
from openai import OpenAI
from langgraph.graph.message import add_messages
import logging
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from langchain.chat_models import init_chat_model
# from math import sum
import time
load_dotenv()
client= OpenAI()

class State(TypedDict):
    messages :Annotated[list,add_messages]

class Cheakponting:
    @tool
    def hi_hello(query : str):
        "you Give onle basic query answers like 'hi','hello','how are you',what is your name ect...." 
        # print(f"toll query:{query}")
        print("⚠️ start hi_hello")
        return query
    
    @tool
    def three_number_add(numbers :list):
        "You calculate of many number with addition"
        print("args:",numbers)
        return sum(numbers)
    
    tools=[three_number_add,hi_hello]
    


    def Start_graph(self , cheakpointing):
        # graph
        tool_node=ToolNode(tools=self.tools)
        # print("tools:",tool_node)
        graph_builder= StateGraph(State)
        
        # Node
        print('1')
        graph_builder.add_node("chat_bot",self.chat_bot)
        graph_builder.add_node("tools",tool_node)

        # adge
        print('2')

        graph_builder.add_edge(START,"chat_bot")
        print('3')
        graph_builder.add_conditional_edges(
            "chat_bot",
            tools_condition
        )
        print('4')
        graph_builder.add_edge('tools','chat_bot')
        print('5')
        graph_builder.add_edge("chat_bot",END)

        return graph_builder.compile(cheakpointing)



    def chat_bot(self,state :State):
        llm = init_chat_model(model_provider="openai", model="gpt-4.1")
        llm_with_tools = llm.bind_tools(tools=self.tools)
        query= state['messages']
        
        messages= llm_with_tools.invoke(query)
        return {'messages':[messages]}

    # def compile_graph_with_cheakpointing(self,cheakpointing):
    #     graph_with_cheakpointer = graph_builder.compile()
    #     return graph_with_cheakpointer
def main():
    DB_URL = "mongodb://admin:admin@localhost:27017/"
    config ={ "configurable" :  { "thread_id" : 50}}

    with MongoDBSaver.from_conn_string(DB_URL) as mongo_cheakpointer:
        graph_with_mongo = Cheakponting().Start_graph(mongo_cheakpointer)
        query=input(">> ")
        _state= State(
            messages=[{'role':'user','content':query}],
            )
        # start=Cheakponting().Start_graph()
        result = graph_with_mongo.invoke(_state,config)  # Execute the graph
        # for event in strem.
        if 'messages' in result:
            final_message = result['messages'][-1]
            if hasattr(final_message, 'content'):
                print(final_message.content)
            else:
                print(final_message)
        else:
            print(result)

                
if __name__ == "__main__":
    main()