# main.py

import os
from dotenv import load_dotenv 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 

# LangChain/OpenAI related imports
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI 


# ... (나머지 코드는 동일)

# Load environment variables from .env file (for local testing only)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Read API Key from environment or .env

# Initialize FastAPI application
app = FastAPI()

# --- CORS Configuration ---
# CORS (Cross-Origin Resource Sharing) is essential for allowing the frontend
# (FE, running on a different domain like Vercel) to access this backend API.
origins = [
    "http://localhost:3000", # Local FE development server
    "https://lilyinit.vercel.app", # FE production domain (MUST BE UPDATED)
    "https://lilyinit.github.io", # GitHub Pages portfolio domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"], # Allow all headers
)

# --- Data Models for API Request/Response ---
# Defines the structure of the JSON data expected in the POST request body.
class SummaryRequest(BaseModel):
    document_text: str  # Field to hold the long text to be summarized


# --- API Endpoints ---

@app.get("/")
def read_root():
    """Basic health check endpoint."""
    return {"message": "Lily AI Backend API is running!"}


@app.post("/summarize")
def summarize_document(request: SummaryRequest):
    """
    Summarizes the document text using LangChain and OpenAI.
    """
    # 1. API Key Check
    if not OPENAI_API_KEY:
        # Note: On GCP Cloud Run, the key is passed via environment variables, not .env
        return {"error": "OpenAI API Key is not configured in the environment."}, 500

    try:
        # 2. Initialize LangChain LLM (using GPT-3.5-turbo model)
        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY, temperature=0.7)

        # 3. Define the summarization prompt
        prompt = f"""
        You are an expert summarizer. Based on the document provided below, 
        accurately and concisely summarize the core content. The summary should be 
        written in three paragraphs or less.

        --- Document ---
        {request.document_text}
        """

        # 4. Invoke LLM and get the response
        response = llm.invoke([HumanMessage(content=prompt)])
        
        # 5. Return the result
        return {
            "summary": response.content,
            "original_length": len(request.document_text)
        }
    
    except Exception as e:
        # Return error message for easier debugging
        return {"error": f"An error occurred during summarization: {e}"}, 500