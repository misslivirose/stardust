from pydantic import BaseModel
from typing import List, Optional, Dict

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