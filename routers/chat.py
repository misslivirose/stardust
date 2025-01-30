from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services.chat_history import initialize_room, append_message, update_ai_response, chat_histories
from services.llm import generate_response
from models.schemas import QueryRequest
from services.websocket_manager import WebSocketManager
import logging

websocket_manager = WebSocketManager()

router = APIRouter()

@router.post("/query/stream")
async def process_query_stream(query_request: QueryRequest):
    # Handles query responses from a room
    query = query_request.query
    room_id = query_request.room_id
    session_id = query_request.session_id
    friendly_name = query_request.friendly_name or session_id

    # Initialize room and append the user's message
    initialize_room(room_id)
    append_message(room_id, friendly_name, query)

    # Define the generator to stream the response
    async def stream_response():
        for chunk in generate_response(query, room_id):
            # Extract the "response" field before concatenating or appending
            if isinstance(chunk, dict) and "response" in chunk:
                update_ai_response(room_id, chunk["response"])
                await websocket_manager.broadcast(room_id, {"history": chat_histories[room_id]["history"]})
                logging.info(f"Broadcasted updated history to room {room_id}")
                yield chunk["response"]

    return StreamingResponse(stream_response(), media_type="text/plain")
