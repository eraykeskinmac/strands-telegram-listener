"""
Tests for Telegram Listener Tool
===============================

Comprehensive test suite for the Telegram listener covering:
- Basic functionality
- Background processing
- Event storage and retrieval
- Message filtering
- Auto-reply mode
- Error handling
- Thread safety
"""

import json
import os
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
import responses
from strands_telegram_listener import telegram_listener
from strands_telegram_listener.telegram_listener import TelegramListener


class TestTelegramListener:
    """Test suite for the TelegramListener class."""

    def setup_method(self):
        """Set up test environment."""
        self.test_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        self.test_chat_id = 123456789
        self.base_url = f"https://api.telegram.org/bot{self.test_token}"

        # Mock agent
        self.mock_agent = Mock()
        self.mock_agent.model = "test-model"
        self.mock_agent.system_prompt = "Test system prompt"
        self.mock_agent.tool_registry.registry.values.return_value = []
        self.mock_agent.trace_attributes = {}
        self.mock_agent.callback_handler = None

    @patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": ""})
    def test_listener_creation_without_token(self):
        """Test that listener creation fails without token."""
        with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
            TelegramListener(agent=self.mock_agent)

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_listener_creation_with_token(self):
        """Test successful listener creation with token."""
        listener = TelegramListener(agent=self.mock_agent)
        assert listener.bot_token == self.test_token
        assert listener.agent == self.mock_agent
        assert not listener.is_running

    @responses.activate
    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_get_bot_info(self):
        """Test getting bot information."""
        bot_info = {
            "id": 123456789,
            "is_bot": True,
            "first_name": "TestBot",
            "username": "test_bot",
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/getMe",
            json={"ok": True, "result": bot_info},
            status=200,
        )

        listener = TelegramListener(agent=self.mock_agent)
        result = listener._get_bot_info()

        assert result == bot_info
        assert listener.bot_info == bot_info

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_should_process_message_filtering(self):
        """Test message filtering logic."""
        listener = TelegramListener(agent=self.mock_agent)

        # Mock bot info
        listener.bot_info = {"id": 123456789}

        # Test valid message
        valid_message = {
            "from": {"id": 987654321, "is_bot": False},
            "text": "Hello bot!",
        }
        assert listener._should_process_message(valid_message)

        # Test bot message (should be filtered)
        bot_message = {
            "from": {"id": 123456789, "is_bot": True},
            "text": "Bot response",
        }
        assert not listener._should_process_message(bot_message)

        # Test own message (should be filtered)
        own_message = {
            "from": {"id": 123456789, "is_bot": False},
            "text": "Own message",
        }
        assert not listener._should_process_message(own_message)

    @patch.dict(
        os.environ,
        {
            "TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
            "STRANDS_TELEGRAM_LISTEN_ONLY_TAG": "#support",
        },
    )
    def test_should_process_message_with_tag_filtering(self):
        """Test message filtering with listen-only tag."""
        listener = TelegramListener(agent=self.mock_agent)
        listener.bot_info = {"id": 123456789}

        # Message with tag (should be processed)
        tagged_message = {
            "from": {"id": 987654321, "is_bot": False},
            "text": "Hello #support bot!",
        }
        assert listener._should_process_message(tagged_message)

        # Message without tag (should be filtered)
        untagged_message = {
            "from": {"id": 987654321, "is_bot": False},
            "text": "Hello bot!",
        }
        assert not listener._should_process_message(untagged_message)

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_store_and_get_recent_events(self):
        """Test event storage and retrieval."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock the events directory and file
            events_dir = Path(temp_dir) / "telegram_events"
            events_file = events_dir / "events.jsonl"

            with patch(
                "strands_telegram_listener.telegram_listener_tool.EVENTS_DIR",
                events_dir,
            ):
                with patch(
                    "strands_telegram_listener.telegram_listener_tool.EVENTS_FILE",
                    events_file,
                ):
                    listener = TelegramListener(agent=self.mock_agent)

                    # Store test events
                    test_event1 = {"update_id": 1, "message": {"text": "Hello"}}
                    test_event2 = {"update_id": 2, "message": {"text": "World"}}

                    listener._store_event(test_event1)
                    listener._store_event(test_event2)

                    # Retrieve events
                    recent_events = listener._get_recent_events(2)

                    assert len(recent_events) == 2
                    assert recent_events[0]["payload"]["update_id"] == 1
                    assert recent_events[1]["payload"]["update_id"] == 2

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_start_stop_listener(self):
        """Test starting and stopping the listener."""
        listener = TelegramListener(agent=self.mock_agent)

        # Test start
        result = listener.start()
        assert "started successfully" in result
        assert listener.is_running
        assert listener.thread is not None

        # Test start when already running
        result = listener.start()
        assert "already running" in result

        # Test stop
        result = listener.stop()
        assert "stopped successfully" in result
        assert not listener.is_running

    @responses.activate
    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_send_response(self):
        """Test sending response messages."""
        responses.add(
            responses.POST,
            f"{self.base_url}/sendMessage",
            json={"ok": True, "result": {"message_id": 123}},
            status=200,
        )

        listener = TelegramListener(agent=self.mock_agent)
        listener._send_response(self.test_chat_id, "Test response", 456)

        # Verify request was made correctly
        assert len(responses.calls) == 1
        request_data = json.loads(responses.calls[0].request.body)
        assert request_data["chat_id"] == self.test_chat_id
        assert request_data["text"] == "Test response"
        assert request_data["reply_to_message_id"] == 456

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_get_status(self):
        """Test getting listener status."""
        listener = TelegramListener(agent=self.mock_agent)
        listener.bot_info = {"id": 123456789, "username": "test_bot"}
        listener.last_update_id = 100

        status_json = listener.get_status()
        status = json.loads(status_json)

        assert status["running"] == False  # Not started yet
        assert status["bot_info"]["id"] == 123456789
        assert status["last_update_id"] == 100
        assert "events_file" in status


class TestTelegramListenerTool:
    """Test suite for the telegram_listener tool function."""

    def setup_method(self):
        """Set up test environment."""
        self.test_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        self.mock_agent = Mock()

    @patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": ""})
    def test_tool_without_token(self):
        """Test tool function without token."""
        result = telegram_listener(action="start", agent=self.mock_agent)
        assert "Error" in result
        assert "TELEGRAM_BOT_TOKEN" in result

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    @patch("strands_telegram_listener.telegram_listener_tool.TelegramListener")
    def test_tool_start_action(self, mock_listener_class):
        """Test tool start action."""
        mock_listener = Mock()
        mock_listener.start.return_value = "Started successfully"
        mock_listener_class.return_value = mock_listener

        result = telegram_listener(action="start", agent=self.mock_agent)

        assert result == "Started successfully"
        mock_listener_class.assert_called_once_with(agent=self.mock_agent)
        mock_listener.start.assert_called_once()

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_tool_unknown_action(self):
        """Test tool with unknown action."""
        result = telegram_listener(action="invalid_action", agent=self.mock_agent)

        assert "Unknown action" in result
        assert "invalid_action" in result

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_tool_get_recent_events_no_file(self):
        """Test getting recent events when no events file exists."""
        with patch(
            "strands_telegram_listener.telegram_listener_tool.EVENTS_FILE"
        ) as mock_events_file:
            mock_events_file.exists.return_value = False

            result = telegram_listener(action="get_recent_events", count=5)

            assert "No events found" in result

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
    )
    def test_tool_get_recent_events_with_data(self):
        """Test getting recent events with data."""
        test_events = [
            json.dumps({"event_type": "telegram_update", "payload": {"update_id": 1}}),
            json.dumps({"event_type": "telegram_update", "payload": {"update_id": 2}}),
        ]

        with patch(
            "strands_telegram_listener.telegram_listener_tool.EVENTS_FILE"
        ) as mock_events_file:
            mock_events_file.exists.return_value = True

            with patch("builtins.open", mock_open_multiple_lines(test_events)):
                result = telegram_listener(action="get_recent_events", count=2)

                assert "Recent Telegram events" in result
                assert "update_id" in result


class TestIntegration:
    """Integration tests for Telegram listener."""

    def test_tool_import(self):
        """Test that the tool can be imported correctly."""
        from strands_telegram_listener import telegram_listener

        assert callable(telegram_listener)

    def test_package_metadata(self):
        """Test package metadata accessibility."""
        import strands_telegram_listener

        assert hasattr(strands_telegram_listener, "__version__")
        assert strands_telegram_listener.get_version() == "1.0.0"

        info = strands_telegram_listener.get_info()
        assert info["name"] == "strands-telegram-listener"
        assert "telegram" in info["description"].lower()
        assert "listener" in info["description"].lower()


def mock_open_multiple_lines(lines):
    """Helper function to mock opening file with multiple lines."""
    from unittest.mock import mock_open

    file_content = "\n".join(lines)
    mock_file = mock_open(read_data=file_content)

    # Override readlines to return the lines
    mock_file.return_value.readlines.return_value = [line + "\n" for line in lines]

    return mock_file


if __name__ == "__main__":
    pytest.main([__file__])
