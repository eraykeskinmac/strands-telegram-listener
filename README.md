# Strands Telegram Listener

[![Awesome Strands Agents](https://img.shields.io/badge/Awesome-Strands%20Agents-00FF77?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjkwIiBoZWlnaHQ9IjQ2MyIgdmlld0JveD0iMCAwIDI5MCA0NjMiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik05Ny4yOTAyIDUyLjc4ODRDODUuMDY3NCA0OS4xNjY3IDcyLjIyMzQgNTYuMTM4OSA2OC42MDE3IDY4LjM2MTZDNjQuOTgwMSA4MC41ODQzIDcxLjk1MjQgOTMuNDI4MyA4NC4xNzQ5IDk3LjA1MDFMMjM1LjExNyAxMzkuNzc1QzI0NS4yMjMgMTQyLjc2OSAyNDYuMzU3IDE1Ni42MjggMjM2Ljg3NCAxNjEuMjI2TDMyLjU0NiAyNjAuMjkxQy0xNC45NDM5IDI4My4zMTYgLTkuMTYxMDcgMzUyLjc0IDQxLjQ4MzUgMzY3LjU5MUwxODkuNTUxIDQxMS4wMDlMMTkwLjEyNSA0MTEuMTY5QzIwMi4xODMgNDE0LjM3NiAyMTQuNjY1IDQwNy4zOTYgMjE4LjE5NiAzOTUuMzU1QzIyMS43ODQgMzgzLjEyMiAyMTQuNzc0IDM3MC4yOTYgMjAyLjU0MSAzNjYuNzA5TDU0LjQ3MzggMzIzLjI5MUM0NC4zNDQ3IDMyMC4zMjEgNDMuMTg3OSAzMDYuNDM2IDUyLjY4NTcgMzAxLjgzMUwyNTcuMDE0IDIwMi43NjZDMzA0LjQzMiAxNzkuNzc2IDI5OC43NTggMTEwLjQ4MyAyNDguMjMzIDk1LjUxMkw5Ny4yOTAyIDUyLjc4ODRaIiBmaWxsPSIjRkZGRkZGIi8+CjxwYXRoIGQ9Ik0yNTkuMTQ3IDAuOTgxODEyQzI3MS4zODkgLTIuNTc0OTggMjg0LjE5NyA0LjQ2NTcxIDI4Ny43NTQgMTYuNzA3NEMyOTEuMzExIDI4Ljk0OTIgMjg0LjI3IDQxLjc1NyAyNzIuMDI4IDQ1LjMxMzhMNzEuMTcyNyAxMDMuNjcxQzQwLjcxNDIgMTEyLjUyMSAzNy4xOTc2IDE1NC4yNjIgNjUuNzQ1OSAxNjguMDgzTDI0MS4zNDMgMjUzLjA5M0MzMDcuODcyIDI4NS4zMDIgMjk5Ljc5NCAzODIuNTQ2IDIyOC44NjIgNDAzLjMzNkwzMC40MDQxIDQ2MS41MDJDMTguMTcwNyA0NjUuMDg4IDUuMzQ3MDggNDU4LjA3OCAxLjc2MTUzIDQ0NS44NDRDLTEuODIzOSA0MzMuNjExIDUuMTg2MzcgNDIwLjc4NyAxNy40MTk3IDQxNy4yMDJMMjE1Ljg3OCAzNTkuMDM1QzI0Ni4yNzcgMzUwLjEyNSAyNDkuNzM5IDMwOC40NDkgMjIxLjIyNiAyOTQuNjQ1TDQ1LjYyOTcgMjA5LjYzNUMtMjAuOTgzNCAxNzcuMzg2IC0xMi43NzcyIDc5Ljk4OTMgNTguMjkyOCA1OS4zNDAyTDI1OS4xNDcgMC45ODE4MTJaIiBmaWxsPSIjRkZGRkZGIi8+Cjwvc3ZnPgo=&logoColor=white)](https://github.com/cagataycali/awesome-strands-agents)

[![PyPI version](https://img.shields.io/pypi/v/strands-telegram-listener.svg)](https://pypi.org/project/strands-telegram-listener/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Real-time Telegram message processing with AI-powered responses for Strands Agents**

A powerful background Telegram message processor that provides seamless real-time messaging capabilities with intelligent AI responses, event storage, and comprehensive message handling for Strands Agents.

## 🚀 Features

### 🎧 **Real-Time Message Processing**
- **Long Polling**: Efficient real-time message retrieval from Telegram
- **Background Processing**: Non-blocking message handling in separate threads
- **Auto-Reply Mode**: AI-powered automatic responses to incoming messages
- **Message Filtering**: Smart filtering to avoid processing own messages
- **Event Storage**: Persistent message history in JSONL format

### 🤖 **AI-Powered Responses**
- **Strands Agent Integration**: Seamless AI response generation
- **Context Awareness**: Maintains conversation context across messages
- **Intelligent Processing**: Advanced message understanding and response
- **Multi-Modal Support**: Text, media, and interactive message handling

### 📊 **Event Management**
- **Persistent Storage**: JSONL-based event logging for history
- **Real-Time Monitoring**: Live status updates and metrics
- **Event Retrieval**: Access to recent message history
- **Thread-Safe Operations**: Concurrent message processing

### 🔧 **Advanced Configuration**
- **Environment-Based Setup**: Easy configuration via environment variables
- **Trigger Keywords**: Optional keyword-based activation
- **Auto-Reply Control**: Toggle automatic responses on/off
- **Listen-Only Mode**: Process messages without responding
- **Comprehensive Logging**: Detailed operation logs

## 📦 Installation

```bash
pip install strands-telegram-listener
```

## 🤖 Bot Setup

Before using this tool, you need to create a Telegram bot and get an API token:

### 1. Create a Telegram Bot

1. **Open Telegram** and search for `@BotFather`
2. **Start a chat** with BotFather by clicking `/start`
3. **Create new bot** with `/newbot` command
4. **Choose a name** for your bot (e.g., "My Awesome Bot")
5. **Choose a username** for your bot (must end with "bot", e.g., "myawesomebot")
6. **Save the token** - BotFather will give you a token like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

### 2. Configure Bot Settings (Optional)

You can customize your bot using BotFather commands:
- `/setdescription` - Set bot description
- `/setcommands` - Set bot commands menu
- `/setprivacy` - Enable/disable privacy mode for groups
- `/setjoingroups` - Allow bot to be added to groups

### 3. Get Your Bot Token

The token from BotFather is your `TELEGRAM_BOT_TOKEN`. Keep it secure!

### 4. Set Environment Variable

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

### 📚 Official Documentation

- **Telegram Bots Guide:** https://core.telegram.org/bots
- **Telegram Bot API:** https://core.telegram.org/bots/api  
- **Full Telegram API:** https://core.telegram.org/api

## 🛠️ Usage

### Quick Start

```python
from strands import Agent
from strands_telegram_listener import telegram_listener

# Create agent with Telegram listener
agent = Agent(tools=[telegram_listener])

# Start listening for messages
agent.tool.telegram_listener(action="start")

# Check listener status
agent.tool.telegram_listener(action="status")

# Get recent events
agent.tool.telegram_listener(action="get_recent_events", count=10)

# Stop listening
agent.tool.telegram_listener(action="stop")
```

### Environment Setup

```bash
# Required: Set your Telegram Bot Token (get from @BotFather)
export TELEGRAM_BOT_TOKEN="your_bot_token_here"

# Optional: Enable automatic AI responses
export STRANDS_TELEGRAM_AUTO_REPLY="true"

# Optional: Only process messages containing this tag
export STRANDS_TELEGRAM_LISTEN_ONLY_TAG="@mybot"

# Optional: Number of events to retrieve by default
export TELEGRAM_DEFAULT_EVENT_COUNT="200"
```

### Advanced Examples

#### Auto-Reply Bot
```python
import os
from strands import Agent
from strands_telegram_listener import telegram_listener

# Enable auto-reply mode
os.environ["STRANDS_TELEGRAM_AUTO_REPLY"] = "true"

# Create intelligent bot agent
agent = Agent(
    system_prompt="""
    You are a helpful Telegram bot assistant. 
    Respond concisely and helpfully to user messages.
    Use appropriate emojis and Telegram formatting.
    """,
    tools=[telegram_listener]
)

# Start listening - bot will automatically respond to messages
agent.tool.telegram_listener(action="start")
print("🤖 AI Bot is now listening and responding!")
```

#### Monitoring Bot
```python
from strands import Agent
from strands_telegram_listener import telegram_listener

# Create monitoring agent (no auto-reply)
agent = Agent(tools=[telegram_listener])

# Start listening in monitor-only mode
agent.tool.telegram_listener(action="start")

# Check status periodically
import time
while True:
    status = agent.tool.telegram_listener(action="status")
    print(f"Bot Status: {status}")
    
    # Get recent messages
    events = agent.tool.telegram_listener(action="get_recent_events", count=5)
    print(f"Recent Events: {events}")
    
    time.sleep(60)  # Check every minute
```

#### Selective Listening
```python
import os
from strands import Agent
from strands_telegram_listener import telegram_listener

# Only process messages containing specific tag
os.environ["STRANDS_TELEGRAM_LISTEN_ONLY_TAG"] = "#support"

agent = Agent(
    system_prompt="You are a customer support bot. Handle support requests professionally.",
    tools=[telegram_listener]
)

# Bot will only respond to messages containing "#support"
agent.tool.telegram_listener(action="start")
```

## 📋 Available Actions

### Core Operations
- `start` - Begin listening for Telegram messages in background
- `stop` - Stop the message listener
- `status` - Get current listener status and configuration  
- `get_recent_events` - Retrieve recent events from storage

### Status Information
The status action returns comprehensive information:
```json
{
  "running": true,
  "bot_info": {
    "id": 123456789,
    "is_bot": true,
    "first_name": "MyBot",
    "username": "my_bot"
  },
  "last_update_id": 123456,
  "events_file": "/path/to/telegram_events/events.jsonl",
  "auto_reply": "true",
  "listen_only_tag": "None"
}
```

## 🔒 Security & Best Practices

### Token Security
- **Never hardcode tokens** in your code
- **Use environment variables** for bot tokens
- **Rotate tokens regularly** for production use
- **Monitor bot permissions** and access logs

### Message Processing
- **Own Message Filtering**: Automatically ignores bot's own messages
- **Duplicate Prevention**: Handles message de-duplication
- **Error Recovery**: Robust error handling with automatic retries
- **Rate Limiting**: Respects Telegram's rate limits

### Production Deployment
```python
# Production configuration example
import os
import logging
from strands import Agent
from strands_telegram_listener import telegram_listener

# Configure logging
logging.basicConfig(level=logging.INFO)

# Production environment variables
os.environ["TELEGRAM_BOT_TOKEN"] = "your_production_token"
os.environ["STRANDS_TELEGRAM_AUTO_REPLY"] = "true"
os.environ["TELEGRAM_DEFAULT_EVENT_COUNT"] = "50"

# Create production agent
agent = Agent(
    system_prompt="""
    Production Telegram Bot Assistant.
    - Respond professionally and helpfully
    - Handle errors gracefully
    - Log important interactions
    - Maintain conversation context
    """,
    tools=[telegram_listener]
)

# Start with error handling
try:
    result = agent.tool.telegram_listener(action="start")
    print(f"✅ Production bot started: {result}")
except Exception as e:
    print(f"❌ Failed to start bot: {e}")
```

## 🎯 Integration Patterns

### With strands-telegram Package
```python
from strands import Agent
from strands_telegram import telegram
from strands_telegram_listener import telegram_listener

# Agent with both tools
agent = Agent(
    system_prompt="You are a comprehensive Telegram bot with full API access.",
    tools=[telegram, telegram_listener]
)

# Start listening
agent.tool.telegram_listener(action="start")

# Bot can now both listen and actively send messages
# The listener will automatically use the telegram tool for responses
```

### Custom Message Processing
```python
from strands import Agent
from strands_telegram_listener import telegram_listener

class CustomTelegramAgent(Agent):
    def process_telegram_message(self, message_data):
        """Custom message processing logic."""
        # Your custom processing here
        user = message_data.get("from", {})
        text = message_data.get("text", "")
        
        # Process with AI
        response = self(f"User {user.get('first_name', 'User')} says: {text}")
        
        # Return response for auto-reply
        return str(response)

agent = CustomTelegramAgent(tools=[telegram_listener])
agent.tool.telegram_listener(action="start")
```

## 📊 Event Storage Format

Events are stored in JSONL format at `./telegram_events/events.jsonl`:

```json
{
  "event_type": "telegram_update",
  "payload": {
    "update_id": 123456,
    "message": {
      "message_id": 789,
      "from": {
        "id": 987654321,
        "is_bot": false,
        "first_name": "John",
        "username": "johndoe"
      },
      "chat": {
        "id": 987654321,
        "first_name": "John",
        "username": "johndoe",
        "type": "private"
      },
      "date": 1697723456,
      "text": "Hello bot!"
    }
  },
  "timestamp": 1697723456.789,
  "update_id": 123456
}
```

## 🔧 Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | - | Bot token from @BotFather |
| `STRANDS_TELEGRAM_AUTO_REPLY` | ❌ No | `false` | Enable automatic AI responses |
| `STRANDS_TELEGRAM_LISTEN_ONLY_TAG` | ❌ No | - | Only process messages with this tag |
| `TELEGRAM_DEFAULT_EVENT_COUNT` | ❌ No | `20` | Default number of events to retrieve |

### Bot Configuration

#### Get Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Use `/newbot` command to create a new bot
3. Follow instructions to set bot name and username
4. Copy the provided bot token
5. Set as `TELEGRAM_BOT_TOKEN` environment variable

#### Bot Permissions
Ensure your bot has appropriate permissions:
- **Send Messages**: Required for auto-reply
- **Read Messages**: Required for message processing
- **Manage Groups**: If using in groups (optional)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
```bash
git clone https://github.com/eraykeskinmac/strands-telegram-listener
cd strands-telegram-listener
pip install -e ".[dev]"
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=strands_telegram_listener

# Run specific test
pytest tests/test_telegram_listener.py::TestTelegramListener::test_start_listener
```

## 📚 API Reference

### telegram_listener(action, count=20, agent=None)

**Parameters:**
- `action` (str): The action to perform
  - `"start"`: Begin listening for messages
  - `"stop"`: Stop the listener
  - `"status"`: Get listener status
  - `"get_recent_events"`: Retrieve recent events
- `count` (int): Number of events to retrieve (for get_recent_events)
- `agent` (Agent): Strands agent instance (auto-provided)

**Returns:**
- `str`: Status message or event data based on the action

## 🔗 Related Packages

- **[strands-telegram](https://pypi.org/project/strands-telegram/)**: Complete Telegram Bot API tool
- **[strands](https://pypi.org/project/strands/)**: Core Strands Agents framework

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [PyPI Package](https://pypi.org/project/strands-telegram-listener/)
- [GitHub Repository](https://github.com/eraykeskinmac/strands-telegram-listener)

## 📞 Support

- Create an issue on GitHub for bug reports
- Join our community discussions for questions
- Check the Strands Agents SDK documentation for integration help

---

**Made with ❤️ for the Strands Agents community**