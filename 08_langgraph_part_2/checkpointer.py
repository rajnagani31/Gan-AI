from langgraph.graph import StateGraph,START,END
from typing import Literal,Annotated
from typing_extensions import TypedDict
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
    message :Annotated[list,add_messages]

class Cheakponting:
    def __init__(self):
        try:
            self.client = client
            self.graph = self.Start_graph()
        except Exception as e:
            logging.error(f"ERROR initializing Withe opanai {e}")

            raise


    @tool
    def hi_hello(query):
        "you Give onle basic query answers like 'hi','hello','how are you',what is your name ect...." 
        # print(f"toll query:{query}")

        return query
    
    @tool
    def three_number_add(*query):
        "You calculate of many number with addition"
        print("args:",query)
        return sum(query)
    
    tools=[three_number_add,hi_hello]
    


    def Start_graph(self):
        # graph
        tool_node=ToolNode(tools=self.tools)
        graph_builder= StateGraph(State)
        
        # Node
        graph_builder.add_node("chat_bot",self.chat_bot)
        graph_builder.add_node("tools",tool_node)

        # adge
        graph_builder.add_edge(START,"chat_bot")
        graph_builder.add_conditional_edges(
            "chat_bot",
            tools_condition
        )
        graph_builder.add_edge('tools','chat_bot')
        graph_builder.add_edge("chat_bot",END)

        return graph_builder.compile()

    llm = init_chat_model(model_provider="openai", model="gpt-4.1")
    llm_with_tools = llm.bind_tools(tools=tools)

    def chat_bot(self,state :State):
        query= state['message']
        # print('query:',query)
        
        messages= self.llm_with_tools.invoke(query)
        # print('messages:',messages)
        # time.sleep(6)
        return {'message':[messages]}

    def run(self,query):
        _state = State(
            message=[{'role':'user','content':query}]
        )
        try:
            print('yes')
            result= self.graph.invoke(_state)
            return result
        except Exception as e:
            print('no')
            logging.error(f"Error invoking the graph: {e}")
            return e
def main():

    query=input(">> ")
    _state= State(
        message=[{'role':'user','content':query}]
    )
    result=Cheakponting().chat_bot(_state)
    # result= Cheakponting().run(query)
    print(result)

main()
# ans=Cheakponting().three_number_add(1,2,3,4,5)
# print(ans)