# flake8: noqa


from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import time
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

# Emedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_db = QdrantVectorStore.from_existing_collection(
    url = "http://vector-db:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

start = time.time()


async def process_query(query: str):
    print("Processing query:", query)
    search_results = vector_db.similarity_search(
    query=query
    )
    
    context = "\n\n\n".join([f"Page Content: {data.page_content}\nPage Number:{data.metadata['page_label']}\nFile Location {data.metadata['source']}" for data in search_results])  
    
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
    print(f"🤖:{query} {response.choices[0].message.content}","\n\n\n")
    time_taken = time.time() - start
    print(f"Time taken to answer the query: {time_taken} seconds")
    print(f"Toke :",response.usage.total_tokens)
    print(f"input Toke :",response.usage.prompt_tokens)
    print(f"output Token :",response.usage.completion_tokens)


    # save to DB
    print()
    return response.choices[0].message.content