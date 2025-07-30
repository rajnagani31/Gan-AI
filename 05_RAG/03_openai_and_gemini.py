from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import os


load_dotenv()
api_key=os.getenv("GEMINI_API_KEY"),
client=OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

pdf_path = Path(__file__).parent / "nodejs.pdf"
print('0')
# Loading
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()  
print('1')

# chunking

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=300,
)

print('2')
split_docs = text_splitter.split_documents(documents=docs)
print("splite ok")
# emmbedding
# embedding_model = OpenAIEmbeddings(
#     model="text-embedding-3-large"
# )
embedding_model = GoogleGenerativeAIEmbeddings(  # gemini function
    model="models/embedding-001",
    google_api_key=api_key
)
print('3')

# vector store

vector_store=QdrantVectorStore(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model

)
print('4')

print("Indexing of Documents Done...")

# embedding
# embedding_model=OpenAIEmbeddings(
#     model="text-embedding-3-large"
# )
embedding_model = GoogleGenerativeAIEmbeddings(  # gemini function
    model="models/embedding-001",
    google_api_key=api_key
)
print('5')
# vector db

vector_db=QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name='learning_vectors',
        embedding=embedding_model,
)
print('6')

query=input(">>")
search_results=vector_db.similarity_search(
    query=query
)
print('7')
context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

# AI work
SYSTEM_PROMPT= f"""
    You are a helpfull AI Assistant who asnweres user query based on the available context
    retrieved from a PDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user
    to open the right page number to know more.

    Context:
    {context}
"""
print('8')

response=client.chat.completions.create(
    model="gemini-2.5-flash-preview-05-20",
    messages=[
        {'role':'system','content':SYSTEM_PROMPT},
        {'role':'user','content':query}
    ]

)
print('9')

print(response.choices[0].message.content)
print('10')

