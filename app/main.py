import os.path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from typing import Optional
from app.manager import ConnectionManager
from app.schemas import ChatMessage
from datetime import datetime
import asyncio

app = FastAPI()
manager = ConnectionManager()


@app.get("/")
async def root():
    return FileResponse(os.path.join("static", "client.html"))


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
    await manager.broadcast(room, join_msg)
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
            await manager.broadcast(room, msg)
    except WebSocketDisconnect:
        # cleanup
        await manager.disconnect(room, websocket)
        leave_msg = ChatMessage(type="leave", username=username, content=f"{username} left", timestamp=datetime.utcnow())
        await manager.broadcast(room, leave_msg)
    except Exception as exc:
        # log and disconnect for any expected error
        await manager.disconnect(room, websocket)
        # optionally broadcast an error message
        err = ChatMessage(type="error", username="server", content=str(exc), timestamp=datetime.utcnow())
        await manager.broadcast(room, err)
