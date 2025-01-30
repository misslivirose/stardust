from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.websocket_manager import WebSocketManager

router = APIRouter()
websocket_manager = WebSocketManager()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):

    await websocket.accept()
    websocket_manager.add_connection(room_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        websocket_manager.remove_connection(room_id, websocket)