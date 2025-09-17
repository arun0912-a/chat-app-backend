from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from manager import ConnectionManager
from app.schemas import ChatMessage
from datetime import datetime
import asyncio

app = FastAPI()
manager =  ConnectionManager()

@app.get("/")
async def root():
    html = open("static/client.html", "r", encoding="utf-8").read()
    return HTMLResponse(html)

@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str, username: Optional[str] = Query("anonymous")):
    """
    Websocket endpoint:
    - client connect to /ws/{room}?username=Alice
    - server receives JSON messages from client, broadcast to room
    - server sends JSON messages to clients
    """
    await manager.connect(room, websocket)
    join_msg = ChatMessage(type="join", username=username, content=f"{username} joined", timestamp=datetime.utcnow())
    # broadcast join message (non-blocking)
    await manager.broadcast(room, join_msg.dict())
    try:
        while True:
            # wait for text message, this is async and non-blocking
            text = await websocket.receive_text()
            # Try to parse as JSON or treat as raw text
            # For simplicity we expect client sends JSON like {"content": "Hello"}
            try:
                import json
                payload = json.loads(text)
                content = payload.get("content", "")
            except Exception:
                content = text

            msg = ChatMessage(
                type="message",
                username=username,
                content=content,
                timestamp=datetime.utcnow()
            )

            # Broadcast to everyone in the room concurrently
            await manager.broadcast(room, msg.dict())
    except WebSocketDisconnect:
        # cleanup
        await manager.disconnect(room, websocket)
        leave_msg = ChatMessage(type="leave", username=username, content=f"{username} left", timstamp=datetime.utcnow())

