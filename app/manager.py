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
