# Stardust Prototype 

# Libraries and Frameworks
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional, Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket, WebSocketDisconnect
import uvicorn
import asyncio
import uuid
import requests
import json
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

active_connections: Dict[str, List[WebSocket]] = {}

# OAuth2 Authentication Stub
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Implement token validation and return the user
    return {"user_id": "sample_user"}  # Placeholder for simplicity

# Models for User Input and Output
class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    room_id: str
    friendly_name: Optional[str] = None


class QueryResponse(BaseModel):
    session_id: str
    room_id: str
    query: str
    retrieved_documents: List[str]
    history: List[Dict[str, str]] 
    generated_response: str

# In-Memory Data Store (Replace with a Database in Production)
data_store = {
    "documents": [
        "Document 1: FastAPI is a modern, fast web framework.",
        "Document 2: OpenAI provides powerful language models.",
        "Document 3: Retrieval-Augmented Generation enhances LLM outputs."
    ]
}

chat_histories = {}

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

@app.post("/query/stream")
async def process_query_stream(query_request: QueryRequest):
    query = query_request.query
    room_id = query_request.room_id
    session_id = query_request.session_id

    # Initialize chat history for the room if it doesn't exist
    if room_id not in chat_histories:
        chat_histories[room_id] = []

    chat_histories[room_id].append({
        "user": f"{query_request.friendly_name or session_id}: {query}",
        "ai": "Stardust: "  # Placeholder until complete response is generated
    })

    async def stream_generate_response(query: str, room_id: str):
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
                        try:
                            json_line = json.loads(parsed_line)
                            if "response" in json_line:
                                chat_histories[room_id][-1]["ai"] += json_line["response"]
                        except json.JSONDecodeError:
                            chat_histories[room_id][-1]["ai"] += parsed_line.strip()
                        await broadcast_updates(room_id)
                        yield parsed_line
                    except Exception as e:
                        yield f"Error parsing response: {str(e)}"

    async def broadcast_updates(room_id: str):
        if room_id in active_connections:
            for connection in active_connections[room_id]:
                try:
                    await connection.send_json({"history": chat_histories[room_id]})
                except Exception as e:
                    logging.error(f"Error broadcasting message: {e}")

    return StreamingResponse(stream_generate_response(query, room_id), media_type="text/plain")



@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)
    try:
        while True:
            # Keep connection alive, waiting for events
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)

async def broadcast_message(room_id: str, message: dict):
    if room_id in active_connections:
        for connection in active_connections[room_id]:
            await connection.send_json(message)

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
