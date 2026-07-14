import os 
from langchain_groq import ChatGroq
from dotenv import load_dotenv 

load_dotenv() 

FAST_MODEL = "llama-3.1-8b-instant"

REASONING_MODEL = "llama-3.3-70b-versatile"

def get_llm(model_name: str = FAST_MODEL):

    return ChatGroq(api_key = os.getenv("GROQ_API_KEY"), model = model_name, temperature=0.0)