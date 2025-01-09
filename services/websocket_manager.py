from fastapi.websockets import WebSocket
from typing import Dict, List
import logging

class WebSocketManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            logging.info("Creating a new WebSocketManager instance")
            cls._instance = super(WebSocketManager, cls).__new__(cls)
            cls._instance.active_connections = {}
        return cls._instance

    def add_connection(self, room_id: str, websocket: WebSocket):
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        logging.info(f"WebSocket connected: {websocket.client} in room {room_id}")

    def remove_connection(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
            logging.info(f"WebSocket disconnected: {websocket.client} from room {room_id}")

    async def broadcast(self, room_id: str, message: dict):
        if room_id in self.active_connections:
            logging.info(f"Broadcasting to room {room_id}: {message}")
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logging.error(f"Error broadcasting to room {room_id}: {e}")
        else:
            logging.warning(f"No active connections in room {room_id}")

