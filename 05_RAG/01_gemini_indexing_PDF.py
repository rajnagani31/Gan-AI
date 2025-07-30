from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
load_dotenv()
client=genai.Client()
api_key = os.getenv("GEMINI_API_KEY")
# client = OpenAI(
#     api_key=api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

pdf_path=Path(__file__).parent/ "nodejs.pdf"

loader= PyPDFLoader(file_path=pdf_path)
docs=loader.load() # Read a file

# Splite docs (chunking)
text_splitter =RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400,
)

split_docs=text_splitter.split_documents(documents=docs)

# vector embedding
embedding_model = GoogleGenerativeAIEmbeddings(  # gemini function
    model="models/embedding-001",
    google_api_key=api_key
)

# Using [embedding_model] create embeddings of [split_docs] and store in DB

vector_store=QdrantVectorStore.from_documents(
        documents=split_docs,
        url="http://localhost:6333",
        collection_name='learning_vectors',
        embedding=embedding_model,

)


print("Indexing of document Done...!")