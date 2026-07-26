from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class LangChainOpenAIAdapter:
    def __init__(self, model: str = "gpt-4.1-mini", temperature: float = None) -> None:
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        
    def bind_tools(self, tools: list):
        client = ChatOpenAI(
            model_name=self.model, 
            api_key=self.api_key,
            temperature=self.temperature,
            # streaming=True,
            )
        print('Binding tools to the LangChainOpenAIAdapter...')
        return client.bind_tools(tools) if tools else client
            
