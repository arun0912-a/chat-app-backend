# 💬 Chat App Backend — FastAPI + WebSockets

A **real-time chat backend** built with [FastAPI](https://fastapi.tiangolo.com/) using **WebSockets**.
This project demonstrates **asynchronous programming in Python**, including concurrency patterns like `async/await`, `asyncio.Lock`, and `asyncio.gather`.

It’s minimal, beginner-friendly, and ready to extend with authentication, persistence, or scaling via Redis.

---

## 🚀 Features

* **Real-time chat** with WebSockets.
* **Room support**: multiple users can chat in the same room.
* **Async-first design**: efficient handling of many simultaneous connections.
* **Connection manager**: concurrency-safe tracking of users in each room.
* **Broadcast system**: sends messages to all connected clients concurrently.
* **Minimal client included**: test quickly in your browser.

---

## 📂 Project Structure

```
chat-backend/
├─ app/
│  ├─ main.py          # FastAPI app & websocket routes
│  ├─ manager.py       # Async connection manager
│  ├─ schemas.py       # Pydantic models for messages
│  └─ __init__.py
├─ static/
│  └─ client.html      # Minimal JS client for testing
├─ requirements.txt
└─ README.md
```

---

## ⚙️ Requirements

* Python **3.10+**
* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/chat-backend.git
   cd chat-backend
   ```

2. Create & activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
   ```

3. Start the server:

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. Open your browser and test:
   👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

   Open multiple tabs, choose the same room, and chat in real time.

---

## 🧑‍💻 Example Usage

* Connect to `/ws/{room}?username=Alice` via WebSocket.
* Send a message:

  ```json
  { "content": "Hello world!" }
  ```
* Receive broadcasted messages in JSON:

  ```json
  {
    "type": "message",
    "username": "Alice",
    "content": "Hello world!",
    "timestamp": "2025-09-17T15:23:45.123Z"
  }
  ```

---

## 📖 How It Works

* **`async def` & `await`**: enables non-blocking I/O.
* **`asyncio.Lock`**: prevents race conditions when modifying active connections.
* **`asyncio.gather`**: broadcasts to all clients concurrently.
* **WebSocket lifecycle**:

  * Accept → Listen → Broadcast → Handle Disconnect.

---

## 🔮 Next Steps / Improvements

* ✅ Add authentication (JWT or OAuth2).
* ✅ Persist chat history (PostgreSQL, MongoDB, or Redis).
* ✅ Scale with Redis Pub/Sub for multi-instance deployment.
* ✅ Add typing indicators & user presence.
* ✅ Build a modern frontend with React or Vue.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add some feature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

✨ Built with FastAPI, Uvicorn, and a love for async programming.

---
