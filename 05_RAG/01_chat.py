from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
from google import genai
load_dotenv()



client=genai.Client()
api_key = os.getenv("GEMINI_API_KEY")
print('1')


embedding_model = GoogleGenerativeAIEmbeddings(  # gemini functionality
    model="models/embedding-001",
     google_api_key=api_key,
)
print('2')

vector_db=QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name='learning_vectors',
        embedding=embedding_model,
)
print('3')



query=input(">>")
search_results=vector_db.similarity_search(
    query=query
)
print('4')
context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])
print('5')

# AI work
system_instruction= f"""
    You are a helpfull AI Assistant who asnweres user query based on the available context
    retrieved from a PDF file along with page_contents and page number.

    give details wirth explainnetion

    You should only ans the user based on the following context and navigate the user
    to open the right page number to know more.
    
    Avoid using Markdown formatting like **bold**, *italic*, or bullet points. Respond in plain, readable sentences.

    Context:
    {context}
"""
prompt=f"""
[system_instruction]
{system_instruction}

[query]
{query}
"""

print('6')

response = client.models.generate_content(
    model="models/gemini-1.5-flash",
    contents=[
        prompt
    ]
)
print('7')

print(f"🤖: {response.text}")

