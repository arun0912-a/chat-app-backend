import json
from fastapi import WebSocket
from typing import Dict, List
from app.schemas import ChatMessage
from datetime import datetime


class ConnectionManager:
    def __init__(self):
        # Store connections grouped by room
        self.active_connections: dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket, username: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

        # 🔔 Notify room: system join message
        join_msg = ChatMessage(
            type="system",
            username="system",
            content=f"👋 {username} joined the room.",
            timestamp=datetime.utcnow()
        )
        await self.broadcast(room, join_msg)

    async def disconnect(self, room: str, websocket: WebSocket, username: str = "unknown"):
        if room in self.active_connections:
            if websocket in self.active_connections[room]:
                self.active_connections[room].remove(websocket)

            if not self.active_connections[room]:
                del self.active_connections[room]

        # 🔔 Notify room: system leave message
        leave_msg = ChatMessage(
            type="system",
            username="system",
            content=f"❌ {username} left the room.",
            timestamp=datetime.utcnow()
        )
        await self.broadcast(room, leave_msg)

    async def broadcast(self, room: str, message: ChatMessage):
        """
        Broadcast a ChatMessage object to all clients in the room.
        """
        if room not in self.active_connections:
            return

        # Pydantic's JSON serialization
        text = message.model_dump_json()

        for ws in list(self.active_connections[room]):
            try:
                await ws.send_text(text)
            except Exception:
                # If sending fails, disconnect client
                await self.disconnect(room, ws)
