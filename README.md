# WebChat 💬

A simple, real-time web chat application built with Flask and Socket.IO.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- 🚀 **Real-time messaging** - Instant message delivery using WebSockets
- 👥 **User presence** - See who's online
- ✍️ **Typing indicators** - Know when someone is typing
- 📜 **Message history** - View previous messages when joining
- 📱 **Responsive design** - Works on desktop and mobile
- 🎨 **Modern UI** - Clean, intuitive interface

## Demo

```
┌─────────────────────────────────────────────────┐
│  💬 WebChat        #general                      │
├──────────┬──────────────────────────────────────┤
│          │  Alice: Hi everyone!        10:23   │
│ ONLINE   │                                       │
│  Users   │  You: Hey Alice!            10:24   │
│          │                                       │
│ ● Alice  │  Bob is typing...                   │
│ ● Bob    │                                       │
│ ● You    │  [Type a message...]        [Send]  │
└──────────┴──────────────────────────────────────┘
```

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/witzwp/webchat.git
cd webchat

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## Usage

### Run the Server

```bash
# Basic usage
webchat

# Or with environment variables
export PORT=8080
export HOST=0.0.0.0
export FLASK_DEBUG=true
webchat
```

### Access the Chat

Open your browser and go to: `http://localhost:5000`

1. Enter your username
2. Click "Join Chat"
3. Start chatting!

## Development

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black src tests
```

### Type Checking

```bash
mypy src
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5000 | Server port |
| `HOST` | 0.0.0.0 | Server host |
| `FLASK_DEBUG` | false | Enable debug mode |
| `SECRET_KEY` | dev-secret-key | Flask secret key |

## Project Structure

```
.
├── src/webchat/              # Main application
│   ├── __init__.py
│   ├── app.py                # Flask & SocketIO server
│   ├── templates/
│   │   └── index.html        # Main chat interface
│   └── static/
│       ├── css/style.css     # Styles
│       └── js/chat.js        # Client-side JavaScript
├── tests/
│   └── test_app.py           # Test suite
├── .github/workflows/
│   └── ci.yml                # GitHub Actions CI
├── pyproject.toml            # Project configuration
└── README.md
```

## Technology Stack

- **Backend**: Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Real-time**: Socket.IO, WebSockets
- **Server**: Eventlet (production-ready)

## API Events

### Client → Server

| Event | Data | Description |
|-------|------|-------------|
| `join` | `{username: string}` | Join the chat |
| `message` | `{message: string}` | Send a message |
| `typing` | `{typing: boolean}` | Typing indicator |

### Server → Client

| Event | Data | Description |
|-------|------|-------------|
| `user_joined` | `{username, users, message}` | User joined |
| `user_left` | `{username, users}` | User left |
| `new_message` | `{username, message, timestamp}` | New message |
| `history` | `{messages: array}` | Message history |
| `user_typing` | `{username, typing}` | Typing status |

## License

MIT License - see [LICENSE](LICENSE) file
