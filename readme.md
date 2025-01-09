# Project Stardust

Project Stardust is a multi-user agent prototype. It supports message synchronization between users in a room and generates AI responses using Ollama.

## Features
1. Multi-User Chat: Users in the same room can communicate in real time.

1. AI Integration: Queries in the chat are processed by Ollama, and AI responses are broadcast to all users.

1. Real-Time Updates: Messages are synchronized across all clients in a room via WebSockets.

1. Custom User Names: Users can set a friendly name that appears in the chat.

1. Room-Based Chats: Messages are isolated by rooms, allowing for separate conversations.

## Project Structure
```
chat-app/
├── app.py                 # Main application entry point
├── routers/
│   ├── chat.py            # Chat-related endpoints
│   ├── websockets.py      # WebSocket endpoints
├── services/
│   ├── llm.py             # LLM API integration
│   ├── chat_history.py    # Chat history management
│   ├── websocket_manager.py # WebSocket connection manager
├── static/
│   ├── js/
│   │   ├── chatBox.js      # Frontend logic for rendering messages
│   │   ├── session.js      # Session management
│   │   ├── query.js        # Query handling
│   │   ├── websocket.js    # WebSocket frontend logic
│   │   └── main.js         # Application initializer
│   └── css/
│       └── style.css       # Styling for the chat interface
├── templates/
│   └── index.html         # Frontend template
└── README.md              # Project documentation
```

