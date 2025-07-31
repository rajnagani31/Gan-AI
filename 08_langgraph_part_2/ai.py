from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from google import genai
from dotenv import load_dotenv
from google.genai.types import GenerateContentConfig
# from langchain_google_genai import ChatGoogleGenerativeAI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()



class State(TypedDict):
    query: str
    llm_result: str | None
    error : str | None      

class CodingQueryGraph:
    def __init__(self):
        """Initializes the graph."""
        try:
            self.client = genai.Client()
            self.graph = self._build_graph()
        except Exception as e:
            logger.error(f"Error initializing Google GenAI client: {e}")
            raise

    def _build_graph(self):
        """Builds and compiles the LangGraph graph."""
        graph_builder = StateGraph(State)
        graph_builder.add_node("chat_bot", self.chat_bot)
        graph_builder.add_edge(START, "chat_bot")
        graph_builder.add_edge("chat_bot", END)
        return graph_builder.compile()

    def chat_bot(self, state: State) -> State:
        """Node to interact with the LLM."""
        query=state['query']
        try:
            model = self.client.get_generative_model("gemini-1.5-flash")
            response = model.generate_content(
                query,
                generation_config=GenerateContentConfig(response_mime_type="text"),
                system_instruction="You only give answers to coding queries. For any other type of question, politely decline."
            )

            if response.text:
                state['llm_result'] = response.text
                state['error'] = None
            else:
                state['llm_result'] = "Sorry, I could not generate a response."
                state['error'] = "Empty response from Google GenAI"
            
        except Exception as e:
            logger.error(f"Error generating content with Google GenAI: {e}")
            state['llm_result'] = None
            state['error'] = str(e)
        return state

    def run(self, query: str):
        """Runs the graph with the given query."""
        _state: State = {"query": query, "llm_result": None, "error": None}
        try:
            response = self.graph.invoke(_state)
            return response
        except Exception as e:
            logger.error(f"Graph invocation failed: {e}")
            return {"query": query, "llm_result": None, "error": str(e)}


def main():
    try:
        query = input("Ask a coding question: ")
        my_graph = CodingQueryGraph()
        result = my_graph.run(query)
        
        if result.get("error"):
            print(f"An error occurred: {result['error']}")
        elif result.get("llm_result"):
            print("\n--- AI Response ---")
            print(result['llm_result'])
            print("-------------------\n")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
