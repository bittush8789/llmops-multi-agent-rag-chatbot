import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, 'chroma_db')

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if not os.path.exists(CHROMA_DIR):
        raise Exception("Chroma DB not found. Please run ingest.py first.")
        
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    
    # Use top_k = 4 as specified
    return vectorstore.as_retriever(search_kwargs={"k": 8})

def retrieve_context(query: str):
    retriever = get_retriever()
    docs = retriever.invoke(query)
    
    # Format the retrieved documents
    context = ""
    sources = set()
    for doc in docs:
        context += f"Source: {doc.metadata.get('source', 'Unknown')}\nContent: {doc.page_content}\n\n"
        source_name = os.path.basename(doc.metadata.get('source', 'Unknown'))
        sources.add(source_name)
        
    return context, list(sources)
