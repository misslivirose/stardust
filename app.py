# Stardust Prototype 

# Libraries and Frameworks
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import asyncio
import uuid
import requests
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI Application
app = FastAPI()

# Configure CORS (for Frontend Integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# OAuth2 Authentication Stub
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Implement token validation and return the user
    return {"user_id": "sample_user"}  # Placeholder for simplicity

# Models for User Input and Output
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

class QueryResponse(BaseModel):
    user_id: str
    query: str
    retrieved_documents: List[str]
    generated_response: str

# In-Memory Data Store (Replace with a Database in Production)
data_store = {
    "documents": [
        "Document 1: FastAPI is a modern, fast web framework.",
        "Document 2: OpenAI provides powerful language models.",
        "Document 3: Retrieval-Augmented Generation enhances LLM outputs."
    ]
}

# Placeholder for Document Vectorization and Search (Implement FAISS, Pinecone, etc.)
def retrieve_documents(query: str, top_k: int = 3):
    # Simple keyword-based retrieval for demonstration
    return [doc for doc in data_store["documents"] if query.lower() in doc.lower()][:top_k]

# Placeholder for LLM Integration (OpenAI Example)
def generate_response(query: str, retrieved_docs: List[str]):
    prompt = f"{query}"

    # Send the prompt to the Ollama server
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt},  # Replace 'llama3.2' with your desired model
        stream=True  # Enable streaming
    )

    if response.status_code == 200:
        result = ""
        for line in response.iter_lines():
            if line:
                try:
                    parsed_line = line.decode("utf-8")
                    result += parsed_line
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error parsing streamed response: {str(e)}")
        return result
    else:
        raise HTTPException(status_code=500, detail=f"Ollama Error: {response.text}")

@app.post("/query", response_model=QueryResponse)
def process_query(query_request: QueryRequest):
    query = query_request.query
    print(query)

    # Retrieve relevant documents
    # retrieved_docs = retrieve_documents(query)

    # if not retrieved_docs:
        # raise HTTPException(status_code=404, detail="No relevant documents found.")

    # Generate a response using retrieved documents
    generated_response = generate_response(query, [])

    return QueryResponse(
        user_id="anonymous_user",  # Simplified user ID for now
        query=query,
        retrieved_documents=retrieved_docs,
        generated_response=generated_response
    )
    
async def stream_generate_response(query: str):
    url = "http://localhost:11434/api/generate"
    params = {"model": "llama3.2", "prompt": query}
    
    with requests.post(url, json=params, stream=True) as response:
        if response.status_code != 200:
            yield f"Ollama Error: {response.text}"
            return

        for line in response.iter_lines():
            if line:
                try:
                    parsed_line = line.decode("utf-8")
                    yield parsed_line
                except Exception as e:
                    yield f"Error parsing response: {str(e)}"

@app.post("/query/stream")
async def process_query_stream(query_request: QueryRequest):
    query = query_request.query
    return StreamingResponse(
        stream_generate_response(query),
        media_type="text/plain"
    )


# Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Run the Application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
