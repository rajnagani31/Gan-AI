from google import genai
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as ge

load_dotenv()
# client=genai.Client()

class State(TypedDict):
    messages:Annotated[list,add_messages]

llm = init_chat_model("openai:gpt-4.1")


def chat_bot(state :State):
    result=llm.invoke(state['messages'])
    return result

# Graph
graph_builder=StateGraph(State)


# Nodes
graph_builder.add_node("chat_bot",chat_bot)

# adge

graph_builder.add_edge(START,"chat_bot")
graph_builder.add_edge("chat_bot",END)

graph=graph_builder.compile()

user_input = "I need some expert guidance for building an AI agent. Could you request assistance for me?"
config = {"configurable": {"thread_id": "1"}}

events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()