"""
Strands Telegram Listener - Real-time Telegram message processing for Strands Agents
===================================================================================

This package provides a powerful background Telegram message processor that enables
real-time messaging capabilities with intelligent AI responses, event storage, and
comprehensive message handling for Strands Agents.

Key Features:
- Real-time message processing with long polling
- AI-powered automatic responses
- Background processing in separate threads
- Event storage and history management
- Smart message filtering and de-duplication
- Comprehensive configuration options
- Thread-safe operations

Quick Start:
-----------
```python
from strands import Agent
from strands_telegram_listener import telegram_listener

# Create agent with Telegram listener
agent = Agent(tools=[telegram_listener])

# Start listening for messages
agent.tool.telegram_listener(action="start")

# Check status
agent.tool.telegram_listener(action="status")

# Get recent events
agent.tool.telegram_listener(action="get_recent_events", count=10)

# Stop listening
agent.tool.telegram_listener(action="stop")
```

Environment Setup:
-----------------
Set your Telegram Bot Token and configuration:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export STRANDS_TELEGRAM_AUTO_REPLY="true"  # Enable AI responses
export STRANDS_TELEGRAM_LISTEN_ONLY_TAG="@mybot"  # Optional tag filtering
```

Auto-Reply Bot Example:
---------------------
```python
import os
from strands import Agent
from strands_telegram_listener import telegram_listener

# Enable auto-reply mode
os.environ["STRANDS_TELEGRAM_AUTO_REPLY"] = "true"

# Create intelligent bot
agent = Agent(
    system_prompt="You are a helpful Telegram bot assistant.",
    tools=[telegram_listener]
)

# Start listening - bot will automatically respond
agent.tool.telegram_listener(action="start")
```

For more examples and documentation, visit:
https://github.com/eraykeskinmac/strands-telegram-listener
"""

from .telegram_listener import telegram_listener

__version__ = "1.0.0"
__author__ = "Strands Community"
__email__ = "community@strandsagents.com"

__all__ = ["telegram_listener"]


# Package metadata
def get_version():
    """Get package version."""
    return __version__


def get_info():
    """Get package information."""
    return {
        "name": "strands-telegram-listener",
        "version": __version__,
        "description": "Real-time Telegram message processing with Strands Agents",
        "author": __author__,
        "email": __email__,
        "url": "https://github.com/eraykeskinmac/strands-telegram-listener",
    }
