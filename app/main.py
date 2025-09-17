from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from app.manager import ConnectionManager
from app.schemas import ChatMessage
from datetime import datetime
import json

app = FastAPI()
manager = ConnectionManager()


@app.get("/")
async def root():
    # Serve client.html from static folder
    html = open("static/client.html", "r", encoding="utf-8").read()
    return HTMLResponse(html)


@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str, username: Optional[str] = Query("guest")):
    """
    WebSocket endpoint:
    - Clients connect to /ws/{room}?username=Alice
    - Server receives JSON messages, broadcasts to room
    - Server sends JSON messages to all clients
    """
    await manager.connect(room, websocket, username)

    try:
        while True:
            # wait for text message
            text = await websocket.receive_text()

            # Parse JSON payload or fallback to raw text
            try:
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

            # Broadcast message to everyone in the room
            await manager.broadcast(room, msg)

    except WebSocketDisconnect:
        await manager.disconnect(room, websocket, username)

    except Exception as exc:
        # handle unexpected errors
        await manager.disconnect(room, websocket, username)
        err = ChatMessage(
            type="error",
            username="server",
            content=str(exc),
            timestamp=datetime.utcnow()
        )
        await manager.broadcast(room, err)
