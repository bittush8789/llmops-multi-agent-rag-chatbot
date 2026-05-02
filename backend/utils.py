import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm(model_name="llama-3.3-70b-versatile"):
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    
    return ChatGroq(
        temperature=0,
        model_name=model_name,
        groq_api_key=groq_api_key
    )
