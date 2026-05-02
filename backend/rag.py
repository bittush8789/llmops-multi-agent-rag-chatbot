import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

CHROMA_PATH = "chroma_db"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vectorstore():
    embeddings = get_embeddings()
    if os.path.exists(CHROMA_PATH):
        return Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return None

def get_retriever():
    vectorstore = get_vectorstore()
    if vectorstore:
        return vectorstore.as_retriever(search_kwargs={"k": 8})
    return None

def retrieve_context(query: str):
    retriever = get_retriever()
    if not retriever:
        return "No context found.", []
    
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
    
    return context, sources
