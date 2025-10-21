"""
Telegram Listener Tool for Strands Agents
========================================

Real-time Telegram message processing with AI-powered responses.

This module provides comprehensive Telegram Bot API integration with:
1. Real-time message polling and processing
2. Background event processing via threading
3. Event history storage and retrieval
4. Agent delegation for intelligent responses
5. Auto-reply mode control
6. Comprehensive error handling

Key Features:
------------
- Long polling for real-time message processing
- Automatic message processing with Strands agents
- Event storage in JSONL format for history
- Configurable auto-reply mode
- Thread-safe background processing
- Message filtering and de-duplication
- Rich error handling and logging

Setup Requirements:
-----------------
1. Telegram Bot Token (from @BotFather)
2. Environment variables:
   - TELEGRAM_BOT_TOKEN: Bot token from @BotFather
   - STRANDS_TELEGRAM_AUTO_REPLY (optional): Set to "true" to enable auto-replies
   - STRANDS_TELEGRAM_LISTEN_ONLY_TAG (optional): Only process messages with this tag
   - TELEGRAM_DEFAULT_EVENT_COUNT (optional): Number of events to retrieve (default: 20)

Usage Examples:
-------------
```python
from strands import Agent
from strands_telegram_listener import telegram_listener

# Create agent with Telegram listener
agent = Agent(tools=[telegram_listener])

# Start listening for messages
result = agent.tool.telegram_listener(action="start")

# Check listener status
status = agent.tool.telegram_listener(action="status")

# Get recent events
events = agent.tool.telegram_listener(action="get_recent_events", count=10)

# Stop the listener
result = agent.tool.telegram_listener(action="stop")

# Toggle auto-reply mode
agent.tool.environment(action="set", name="STRANDS_TELEGRAM_AUTO_REPLY", value="true")
```

Event Processing Flow:
--------------------
1. Long polling retrieves new messages from Telegram
2. Messages are filtered (own messages, duplicates)
3. Events stored to local filesystem
4. Message processed by Strands agent
5. Response sent back to Telegram (if auto-reply enabled)
6. Processing status tracked and logged

Auto-Reply Mode:
--------------
Control automatic response behavior:
- STRANDS_TELEGRAM_AUTO_REPLY=true: Agent automatically sends responses
- Default (false): Agent processes but doesn't respond automatically

Real-time events stored at: ./telegram_events/events.jsonl
"""

import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from strands import Agent, tool

# Configure logging
logger = logging.getLogger(__name__)

# System prompt for Telegram communications
TELEGRAM_SYSTEM_PROMPT = """
You are an AI assistant integrated with Telegram. Important guidelines:

1. MESSAGE IDENTIFICATION:
   - You'll receive ALL messages including your own echoed back
   - NEVER respond to your own messages - check bot info carefully
   - Your messages have "from": {"is_bot": true} field
   - The bot's user_id is available in bot_info

2. INTERACTION CAPABILITIES:
   - Send messages with telegram(action="send_message", chat_id="...", text="...")
   - Send photos with telegram(action="send_photo", chat_id="...", file_path="...")
   - Send documents with telegram(action="send_document", chat_id="...", file_path="...")
   - Create polls with telegram(action="send_poll", chat_id="...", question="...", options=[...])
   - Send locations with telegram(action="send_location", chat_id="...", latitude=x, longitude=y)

3. CONVERSATION FLOW:
   - Maintain context across messages
   - Use reply_to_message_id for threaded conversations
   - Keep responses concise and chat-appropriate

4. CONTENT GUIDELINES:
   - Use Telegram formatting: *bold*, _italic_, `code`, ```code blocks```
   - Support emojis and Unicode
   - Keep messages under 4096 characters
   - Use appropriate Telegram features (polls, keyboards, etc.)

Use telegram tool to communicate back to users.
"""

# Event storage configuration
EVENTS_DIR = Path.cwd() / "telegram_events"
EVENTS_FILE = EVENTS_DIR / "events.jsonl"

# Make sure events directory exists
EVENTS_DIR.mkdir(parents=True, exist_ok=True)

# Global variables for the listener
listener_thread: Optional[threading.Thread] = None
is_listening: bool = False
bot_info: Optional[Dict] = None
last_update_id: int = 0


class TelegramListener:
    """
    Real-time Telegram message processor with agent integration.

    This class handles long polling from Telegram's getUpdates API,
    processes messages through Strands agents, and manages event storage.
    """

    def __init__(self, agent=None):
        self.agent = agent
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.is_running = False
        self.thread = None
        self.bot_info = None
        self.last_update_id = 0

        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

    def _get_bot_info(self) -> Dict:
        """Get bot information from Telegram API."""
        if self.bot_info is None:
            try:
                response = requests.get(
                    f"https://api.telegram.org/bot{self.bot_token}/getMe", timeout=10
                )
                if response.status_code == 200:
                    self.bot_info = response.json().get("result", {})
                else:
                    logger.error(f"Error getting bot info: {response.text}")
                    self.bot_info = {}
            except Exception as e:
                logger.error(f"Error getting bot info: {e}")
                self.bot_info = {}
        return self.bot_info

    def _store_event(self, event_data: Dict):
        """Store event to local filesystem."""
        try:
            event_record = {
                "event_type": "telegram_update",
                "payload": event_data,
                "timestamp": time.time(),
                "update_id": event_data.get("update_id"),
            }

            EVENTS_DIR.mkdir(parents=True, exist_ok=True)
            with open(EVENTS_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_record, ensure_ascii=False) + "\n")

        except Exception as e:
            logger.error(f"Error storing event: {e}")

    def _should_process_message(self, message: Dict) -> bool:
        """Determine if message should be processed."""
        # Skip if no message
        if not message:
            return False

        # Skip our own messages
        if message.get("from", {}).get("is_bot"):
            return False

        # Skip if from our bot user
        bot_info = self._get_bot_info()
        if message.get("from", {}).get("id") == bot_info.get("id"):
            return False

        # Check for listen-only tag
        listen_only_tag = os.environ.get("STRANDS_TELEGRAM_LISTEN_ONLY_TAG")
        message_text = message.get("text", "")
        if listen_only_tag and listen_only_tag not in message_text:
            return False

        return True

    def _process_message(self, message: Dict):
        """Process a message using Strands agent."""
        if not self.agent:
            logger.error("No agent available for message processing")
            return

        try:
            # Extract message details
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")
            user = message.get("from", {})
            message_id = message.get("message_id")

            # Get recent events for context
            event_count = int(os.getenv("TELEGRAM_DEFAULT_EVENT_COUNT", "200"))
            recent_events = self._get_recent_events(event_count)
            event_context = (
                f"\nRecent Telegram Events: {json.dumps(recent_events)}"
                if recent_events
                else ""
            )

            # Create agent with Telegram system prompt
            tools = list(self.agent.tool_registry.registry.values())
            trace_attributes = self.agent.trace_attributes

            agent = Agent(
                model=self.agent.model,
                messages=[],
                system_prompt=f"{self.agent.system_prompt}\n{TELEGRAM_SYSTEM_PROMPT}",
                tools=tools,
                callback_handler=self.agent.callback_handler,
                trace_attributes=trace_attributes,
            )

            # Add event context to system prompt
            agent.system_prompt = (
                f"{TELEGRAM_SYSTEM_PROMPT}\n\nEvent Context:\n"
                f"Current: {json.dumps(message)}{event_context}"
            )

            # Process message with agent
            user_name = user.get("first_name", "User")
            username = user.get("username", "")
            user_display = f"{user_name} (@{username})" if username else user_name

            prompt = f"[Chat ID: {chat_id}] {user_display} says: {text}"
            response = agent(prompt)

            # Send response if auto-reply is enabled
            if response and str(response).strip():
                auto_reply = (
                    os.getenv("STRANDS_TELEGRAM_AUTO_REPLY", "false").lower() == "true"
                )
                if auto_reply:
                    self._send_response(chat_id, str(response).strip(), message_id)

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)

    def _send_response(self, chat_id: int, text: str, reply_to_message_id: int = None):
        """Send response message to Telegram."""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

            if reply_to_message_id:
                payload["reply_to_message_id"] = reply_to_message_id

            response = requests.post(url, json=payload, timeout=10)
            if response.status_code != 200:
                logger.error(f"Error sending response: {response.text}")

        except Exception as e:
            logger.error(f"Error sending response: {e}")

    def _get_recent_events(self, count: int) -> List[Dict[str, Any]]:
        """Get recent events from storage."""
        if not EVENTS_FILE.exists():
            return []

        try:
            with open(EVENTS_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()[-count:]
                events = []
                for line in lines:
                    try:
                        event_data = json.loads(line.strip())
                        events.append(event_data)
                    except json.JSONDecodeError:
                        continue
                return events
        except Exception as e:
            logger.error(f"Error reading events file: {e}")
            return []

    def _polling_loop(self):
        """Main polling loop for getting updates."""
        logger.info("🚀 Starting Telegram polling loop...")

        while self.is_running:
            try:
                # Get updates from Telegram
                url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
                params = {
                    "offset": self.last_update_id + 1,
                    "timeout": 30,  # Long polling timeout
                    "limit": 100,
                }

                response = requests.get(url, params=params, timeout=35)

                if response.status_code == 200:
                    data = response.json()
                    updates = data.get("result", [])

                    for update in updates:
                        # Store event
                        self._store_event(update)

                        # Update last_update_id
                        self.last_update_id = max(
                            self.last_update_id, update.get("update_id", 0)
                        )

                        # Process message if present
                        if "message" in update:
                            message = update["message"]
                            if self._should_process_message(message):
                                logger.info(
                                    f"Processing message from {message.get('from', {}).get('first_name', 'Unknown')}"
                                )
                                self._process_message(message)

                else:
                    logger.error(f"Error getting updates: {response.text}")
                    time.sleep(5)  # Wait before retrying

            except requests.exceptions.Timeout:
                # Timeout is expected with long polling, continue
                continue
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                time.sleep(5)  # Wait before retrying

        logger.info("✅ Telegram polling loop stopped")

    def start(self):
        """Start the listener in background thread."""
        if self.is_running:
            return "Telegram listener is already running"

        self.is_running = True
        self.thread = threading.Thread(target=self._polling_loop, daemon=True)
        self.thread.start()

        logger.info("✅ Telegram listener started")
        return "✅ Telegram listener started successfully"

    def stop(self):
        """Stop the listener."""
        if not self.is_running:
            return "Telegram listener is not running"

        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)

        logger.info("✅ Telegram listener stopped")
        return "✅ Telegram listener stopped successfully"

    def get_status(self):
        """Get listener status."""
        status = {
            "running": self.is_running,
            "bot_info": self._get_bot_info(),
            "last_update_id": self.last_update_id,
            "events_file": str(EVENTS_FILE),
            "auto_reply": os.getenv("STRANDS_TELEGRAM_AUTO_REPLY", "false"),
            "listen_only_tag": os.getenv("STRANDS_TELEGRAM_LISTEN_ONLY_TAG", "None"),
        }
        return json.dumps(status, indent=2)


# Global listener instance
_telegram_listener: Optional[TelegramListener] = None


@tool
def telegram_listener(action: str, count: int = 20, agent=None) -> str:
    """
    Real-time Telegram message listener with AI-powered responses.

    This tool provides background processing of Telegram messages using
    long polling, with intelligent responses powered by Strands agents.

    Actions:
        start: Begin listening for Telegram messages in background
        stop: Stop the message listener
        status: Get current listener status and configuration
        get_recent_events: Retrieve recent events from storage

    Args:
        action: The action to perform (start, stop, status, get_recent_events)
        count: Number of recent events to retrieve (for get_recent_events)
        agent: Strands agent instance (automatically provided)

    Returns:
        str: Status message or event data based on the action

    Environment Variables:
        TELEGRAM_BOT_TOKEN: Required bot token from @BotFather
        STRANDS_TELEGRAM_AUTO_REPLY: Set to "true" to enable automatic responses
        STRANDS_TELEGRAM_LISTEN_ONLY_TAG: Only process messages containing this tag
        TELEGRAM_DEFAULT_EVENT_COUNT: Default number of events to retrieve

    Examples:
        # Start listening
        telegram_listener(action="start")

        # Check status
        telegram_listener(action="status")

        # Get recent messages
        telegram_listener(action="get_recent_events", count=10)

        # Stop listening
        telegram_listener(action="stop")
    """
    global _telegram_listener

    try:
        # Initialize listener if needed
        if _telegram_listener is None and action in ["start", "status"]:
            _telegram_listener = TelegramListener(agent=agent)

        if action == "start":
            if _telegram_listener is None:
                _telegram_listener = TelegramListener(agent=agent)
            return _telegram_listener.start()

        elif action == "stop":
            if _telegram_listener:
                return _telegram_listener.stop()
            return "No listener running"

        elif action == "status":
            if _telegram_listener:
                return _telegram_listener.get_status()
            return "Listener not initialized"

        elif action == "get_recent_events":
            if not EVENTS_FILE.exists():
                return "No events found in storage"

            try:
                with open(EVENTS_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()[-count:]
                    events = []
                    for line in lines:
                        try:
                            event_data = json.loads(line.strip())
                            events.append(event_data)
                        except json.JSONDecodeError:
                            continue

                    if events:
                        return f"Recent Telegram events:\n{json.dumps(events, indent=2, ensure_ascii=False)}"
                    else:
                        return "No valid events found in storage"
            except Exception as e:
                return f"Error reading events: {e}"

        else:
            return f"Unknown action: {action}. Available: start, stop, status, get_recent_events"

    except Exception as e:
        logger.error(f"Error in telegram_listener: {e}", exc_info=True)
        return f"Error: {str(e)}"
