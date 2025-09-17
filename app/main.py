from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from .manager import ConnectionManager
from .schemas import ChatMessage
from datetime import datetime
import asyncio