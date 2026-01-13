from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()

# oading
path = Path(__file__).parent / "nodejs.pdf"
docs = PyPDFLoader(file_path=path).load()

# Chunking
text_spliter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)

docs_with_spliter = text_spliter.split_documents(documents=docs)

# vector Embeddings
embedding_model =OpenAIEmbeddings(model="text-embedding-3-large")

# using [Embeddings mode] create embedding of spliting and stord in DB

vector_store = QdrantVectorStore.from_documents(
    documents=docs_with_spliter,
    url = "http://localhost:6333",
    collection_name = "learning_vectors",
    embedding = embedding_model
)

print("Indexing of documents Done")
