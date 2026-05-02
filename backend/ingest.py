import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from backend.rag import get_embeddings

load_dotenv()

CHROMA_PATH = "chroma_db"

def ingest_docs():
    print("🚀 Starting Local Ingestion to ChromaDB...")
    
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    loader = DirectoryLoader(docs_dir, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(documents)
    
    embeddings = get_embeddings()
    
    print(f"Indexing {len(splits)} chunks to local ChromaDB...")
    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("✅ Local Ingestion Complete!")

if __name__ == "__main__":
    ingest_docs()
