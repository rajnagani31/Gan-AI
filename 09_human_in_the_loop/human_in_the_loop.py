from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode,tools_condition
from google import genai
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain_core.tools import tool
from langgraph.types import interrupt, Command
import os,json
load_dotenv()

client=genai.Client()
api_key=os.getenv("GEMINI_API_KEY")

class State(TypedDict):
    messages:Annotated[list,add_messages]

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt(
        {"query": query})  # This saves the state in DB and kills the graph
    return human_response["data"]    

tools=[human_assistance]
llm=init_chat_model(model_provider="openai",model="gpt-4.1-nano")
llm_with_tool=llm.bind_tools(tools)

def chat_bot(state:State):
    result=llm_with_tool.invoke(state['messages'])
    return {"messages":[result]}


# gemini ai
# def chat_bot(state:State):
#     query=state['messages']
#     response=client.models.generate_content(
#         model="models/gemini-1.5-flash",
#         contents=[query]
#     )
#     return {'messages':[response]}
# graph
tool_node=ToolNode(tools=tools)
graph_builder=StateGraph(State)

# node

graph_builder.add_node("chat_bot",chat_bot)
graph_builder.add_node("tools",tool_node)

# edges

graph_builder.add_edge(START,'chat_bot')
graph_builder.add_conditional_edges(
    "chat_bot",
    tools_condition
)
graph_builder.add_edge('tools','chat_bot')
graph_builder.add_edge("chat_bot",END)



def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


# user
def main():
    DB_URL="mongodb://admin:admin@localhost:27017" 
    config={"configurable":{"thread_id":21}}
    with MongoDBSaver.from_conn_string(DB_URL) as mongo_check_pointer:
        graph_with_cheak=create_chat_graph(mongo_check_pointer)
        while True:
            query=input(">> ")

            _state=State(
                messages=[{'role':"user",'content':query}]
            )

            

            for event in graph_with_cheak.stream(_state,config,stream_mode='values'):
                if "messages" in event:
                    event["messages"][-1].pretty_print()


# human 
def admin_call():
    DB_URI = "mongodb://admin:admin@localhost:27017"
    config = {"configurable": {"thread_id": "21"}}

    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_cp = create_chat_graph(mongo_checkpointer)

        state = graph_with_cp.get_state(config=config)
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

        for event in graph_with_cp.stream(resume_command, config, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()


      
main()

# admin_call()