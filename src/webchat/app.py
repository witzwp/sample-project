"""Flask application for WebChat."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users and messages (in production, use a database)
connected_users: dict[str, str] = {}
message_history: list[dict[str, Any]] = []
MAX_HISTORY = 100


@app.route("/")
def index() -> str:
    """Render the main chat page."""
    return render_template("index.html")


@socketio.on("connect")
def handle_connect() -> None:
    """Handle client connection."""
    sid = request.sid  # type: ignore[attr-defined]
    print(f"Client connected: {sid} at {datetime.now()}")


@socketio.on("disconnect")
def handle_disconnect() -> None:
    """Handle client disconnection."""
    sid = request.sid  # type: ignore[attr-defined]
    if sid in connected_users:
        username = connected_users[sid]
        del connected_users[sid]
        emit(
            "user_left",
            {"username": username, "users": list(connected_users.values())},
            broadcast=True,
        )
        print(f"User {username} disconnected")


@socketio.on("join")
def handle_join(data: dict[str, str]) -> None:
    """Handle user joining the chat.

    Args:
        data: Dictionary containing username
    """
    username = data.get("username", "Anonymous").strip()
    if not username:
        username = "Anonymous"

    # Store user
    sid = request.sid  # type: ignore[attr-defined]
    connected_users[sid] = username

    # Join room
    join_room("general")

    # Send welcome message
    emit(
        "user_joined",
        {
            "username": username,
            "users": list(connected_users.values()),
            "message": f"{username} joined the chat",
        },
        broadcast=True,
    )

    # Send message history to new user
    emit("history", {"messages": message_history})


@socketio.on("message")
def handle_message(data: dict[str, str]) -> None:
    """Handle new chat message.

    Args:
        data: Dictionary containing message text
    """
    sid = request.sid  # type: ignore[attr-defined]
    username = connected_users.get(sid, "Anonymous")

    message_text = data.get("message", "").strip()
    if not message_text:
        return

    # Create message object
    message = {
        "username": username,
        "message": message_text,
        "timestamp": datetime.now().isoformat(),
    }

    # Store in history
    message_history.append(message)
    if len(message_history) > MAX_HISTORY:
        message_history.pop(0)

    # Broadcast to all clients
    emit("new_message", message, broadcast=True)


@socketio.on("typing")
def handle_typing(data: dict[str, bool]) -> None:
    """Handle typing indicator.

    Args:
        data: Dictionary containing typing status
    """
    sid = request.sid  # type: ignore[attr-defined]
    username = connected_users.get(sid, "Anonymous")
    is_typing = data.get("typing", False)

    emit(
        "user_typing",
        {"username": username, "typing": is_typing},
        broadcast=True,
        include_self=False,
    )


def main() -> None:
    """Run the Flask-SocketIO server."""
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    print(f"Starting WebChat on http://{host}:{port}")
    print(f"Debug mode: {debug}")
    socketio.run(app, host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
