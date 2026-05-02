import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from backend.rag import get_embeddings

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "technova_enterprise")

def init_qdrant_collection():
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Create collection if not exists
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)
    
    if not exists:
        print(f"Creating collection: {COLLECTION_NAME}")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )

def ingest_docs():
    print("🚀 Starting Production Ingestion to Qdrant Cloud...")
    init_qdrant_collection()
    
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    loader = DirectoryLoader(docs_dir, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    # Process expanded JSON knowledge base if exists
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expanded_knowledge_base.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
            from langchain_core.documents import Document
            for entry in data:
                doc_text = f"Question: {entry['question']}\nAnswer: {entry['answer']}\nCategory: {entry['category']}"
                documents.append(Document(page_content=doc_text, metadata={"source": "expanded_kb", "category": entry["category"]}))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(documents)
    
    embeddings = get_embeddings()
    
    print(f"Indexing {len(splits)} chunks to Qdrant Cloud...")
    QdrantVectorStore.from_documents(
        splits,
        embeddings,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=COLLECTION_NAME,
        force_recreate=True
    )
    print("✅ Ingestion Complete!")

if __name__ == "__main__":
    ingest_docs()
