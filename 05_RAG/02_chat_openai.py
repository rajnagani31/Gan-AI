# build RAG PDF chatbot with OpenAI and LangChain

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
load_dotenv()

client = OpenAI()
# Emedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")


vector_db = QdrantVectorStore.from_existing_collection(
    url = "http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

# Stap 1: Tack User Query

query = input('>>')

# Stap 2 : Vector similarity search [query] in DB

search_results = vector_db.similarity_search(
    query=query
)

context = "\n\n\n".join([f"Page Content: {data.page_content}\nPage Number:{data.metadata['page_label']}\nFile Location {data.metadata['source']}" for data in search_results])

# Stap 3 : Bind User Query + LLM Knowledge

SYSTEM_PROMPT = f"""
        you are an AI assistant Who answers user query based on the context from the document.
        retrieved from a PDF file along with page context and page number.

        you should answer the user based on the following context and nevigation 
        the user  to open the right page number to know more.

        context : {context}
"""

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
)           

print("Chatbot response generated...................................................")
print(f"🤖: {response.choices[0].message.content}")