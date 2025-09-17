import json
from fastapi import WebSocket
from typing import Dict, List
from app.schemas import ChatMessage


class ConnectionManager:
    def __init__(self):
        # Store connections grouped by room
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    async def disconnect(self, room: str, websocket: WebSocket):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def broadcast(self, room: str, message: ChatMessage):
        """
        Broadcast a ChatMessage object to all clients in the room.
        """
        if room not in self.active_connections:
            return

        # Use Pydantic's JSON serialization (handles datetime automatically)
        text = message.model_dump_json()

        for ws in list(self.active_connections[room]):
            try:
                await ws.send_text(text)
            except Exception:
                await self.disconnect(room, ws)
