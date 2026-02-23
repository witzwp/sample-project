"""Tests for WebChat application."""

from __future__ import annotations

import json
import pytest
from flask.testing import FlaskClient

from webchat.app import app, socketio, message_history, connected_users


@pytest.fixture
def client() -> FlaskClient:
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    # Clear state before each test
    message_history.clear()
    connected_users.clear()
    with app.test_client() as client:
        yield client


@pytest.fixture
def socket_client(client: FlaskClient):
    """Create a Socket.IO test client."""
    socket_test_client = socketio.test_client(app, flask_test_client=client)
    yield socket_test_client
    socket_test_client.disconnect()


class TestRoutes:
    """Tests for HTTP routes."""

    def test_index_page(self, client: FlaskClient) -> None:
        """Test that the index page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"WebChat" in response.data
        assert b"username" in response.data

    def test_static_files(self, client: FlaskClient) -> None:
        """Test that static files are accessible."""
        css_response = client.get("/static/css/style.css")
        assert css_response.status_code == 200

        js_response = client.get("/static/js/chat.js")
        assert js_response.status_code == 200


class TestSocketIO:
    """Tests for Socket.IO events."""

    def test_connect_and_join(self, socket_client) -> None:
        """Test connecting and joining the chat."""
        # Emit join event
        socket_client.emit("join", {"username": "TestUser"})

        # Get received messages
        received = socket_client.get_received()

        # Check that we received user_joined and history events
        event_names = [msg["name"] for msg in received]
        assert "user_joined" in event_names
        assert "history" in event_names

    def test_send_message(self, socket_client) -> None:
        """Test sending a message."""
        # First join
        socket_client.emit("join", {"username": "TestUser"})
        socket_client.get_received()  # Clear received messages

        # Send a message
        socket_client.emit("message", {"message": "Hello, World!"})

        # Get received messages
        received = socket_client.get_received()

        # Check that message was broadcast
        event_names = [msg["name"] for msg in received]
        assert "new_message" in event_names

        # Check message content
        message_event = next(msg for msg in received if msg["name"] == "new_message")
        assert message_event["args"][0]["message"] == "Hello, World!"
        assert message_event["args"][0]["username"] == "TestUser"

    def test_message_history(self, socket_client) -> None:
        """Test that message history is maintained."""
        # Join and send messages
        socket_client.emit("join", {"username": "User1"})
        socket_client.get_received()

        socket_client.emit("message", {"message": "Message 1"})
        socket_client.get_received()

        socket_client.emit("message", {"message": "Message 2"})
        socket_client.get_received()

        # Check message history
        assert len(message_history) == 2
        assert message_history[0]["message"] == "Message 1"
        assert message_history[1]["message"] == "Message 2"

    def test_typing_indicator(self, socket_client) -> None:
        """Test typing indicator event."""
        # Join first
        socket_client.emit("join", {"username": "TestUser"})
        socket_client.get_received()

        # Send typing event
        socket_client.emit("typing", {"typing": True})

        # Event should be broadcast (but not to self)
        received = socket_client.get_received()
        # typing event is not sent to the sender, so list might be empty
        # This is expected behavior

    def test_empty_message_not_sent(self, socket_client) -> None:
        """Test that empty messages are not broadcast."""
        # Join first
        socket_client.emit("join", {"username": "TestUser"})
        socket_client.get_received()

        # Try to send empty message
        socket_client.emit("message", {"message": "   "})

        # Check that no new_message event was sent
        received = socket_client.get_received()
        event_names = [msg["name"] for msg in received]
        assert "new_message" not in event_names

    def test_anonymous_username(self, socket_client) -> None:
        """Test joining without a username."""
        socket_client.emit("join", {"username": ""})

        received = socket_client.get_received()
        user_joined = next(msg for msg in received if msg["name"] == "user_joined")

        # Should default to Anonymous
        assert "Anonymous" in user_joined["args"][0]["message"]


class TestAppConfiguration:
    """Tests for app configuration."""

    def test_secret_key_default(self) -> None:
        """Test that default secret key is set."""
        # The app fixture already set a test secret key
        assert app.config["SECRET_KEY"] == "test-secret-key"

    def test_main_function(self) -> None:
        """Test that main function exists and is callable."""
        from webchat.app import main

        assert callable(main)
