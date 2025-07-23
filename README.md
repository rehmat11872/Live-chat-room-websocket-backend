# 🧠 Django Channels WebSocket Backend

This is a simple Django backend with **WebSocket support** using **Django Channels**, meant to work with a basic React frontend. It demonstrates real-time communication via WebSockets, ideal for learning or prototyping chat-like features.

---

## 🚀 Features

- ✅ Real-time WebSocket communication
- ✅ Basic chat room support
- ✅ JSON message handling
- ✅ Group broadcasting with Channels
- ✅ Compatible with React frontend client

---

## 📦 Requirements

- Python 3.8+
- Django 4.x or 5.x
- Django Channels
- Redis (for channel layer)


## commands

-daphne -p 8000 chatproject.asgi:application