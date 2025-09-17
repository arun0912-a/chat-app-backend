from typing import Dict, Set
from fastapi import WebSocket
import asyncio
import json


class ConnectionManager:
    """
    Manage websocket, connection and broadcasting.
    Using asyncio.Lock for concurrency safety when modifying the connection set
    """

    def __init__(self):
        self.active_connections: Dict[str, set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, room: str, websocket: WebSocket):
        """
        Accept the websocket and add to the room set.
        Using a lock ensures that adding/removing connections is safe under concurrency
        """
        await websocket.accept()
        async with self._lock:
            if room not in self.active_connections:
                self.active_connections[room] = set()
            self.active_connections[room].add(websocket)

    async def disconnect(self, room: str, websocket: WebSocket):
        async with self._lock:
            conns = self.active_connections.get(room)
            if conns and websocket in conns:
                conns.remove(websocket)
                if not conns:
                    # remove empty rooms to keep structure tidy
                    del self.active_connections[room]

    async def broadcast(self, room: str, message: dict):
        """
        Broadcast a message dict to every web socket in that room.
        convert to JSON string once for efficiency
        """
        text = json.dumps(message)

