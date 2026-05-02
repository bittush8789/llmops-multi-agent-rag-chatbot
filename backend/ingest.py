import os
import json
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
CHROMA_DIR = os.path.join(BASE_DIR, 'chroma_db')

def load_documents():
    print(f"Loading documents from {DOCS_DIR}")
    documents = []
    
    # Load TXT files
    txt_loader = DirectoryLoader(DOCS_DIR, glob="**/*.txt", loader_cls=TextLoader)
    documents.extend(txt_loader.load())
    
    # Load PDF files if any
    pdf_loader = DirectoryLoader(DOCS_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
    try:
        documents.extend(pdf_loader.load())
    except Exception:
        pass
        
    # Load DOCX files if any
    docx_loader = DirectoryLoader(DOCS_DIR, glob="**/*.docx", loader_cls=Docx2txtLoader)
    try:
        documents.extend(docx_loader.load())
    except Exception:
        pass
        
    # Load JSON knowledge base expansion
    json_path = os.path.join(DOCS_DIR, 'expanded_knowledge_base.json')
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            for item in data:
                text = f"Question: {item['question']}\nAnswer: {item['answer']}"
                documents.append(Document(page_content=text, metadata={"source": "expanded_knowledge_base.json"}))
        print("Loaded expanded knowledge base from JSON.")
        
    print(f"Loaded {len(documents)} documents total.")
    return documents

def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")
    return chunks

def create_vector_db():
    documents = load_documents()
    if not documents:
        print("No documents found. Please add some files to the docs folder.")
        return
        
    chunks = chunk_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print(f"Creating ChromaDB in {CHROMA_DIR}")
    # Create and persist the vector database
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print("Vector database created successfully.")

if __name__ == "__main__":
    create_vector_db()
