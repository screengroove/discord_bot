# Discord Bot

A versatile Discord bot built with Python and discord.py, featuring both Discord-native commands and OpenAI integration.

## Features

- **Basic Bot Commands** ([bot.py](bot.py)) - Core functionality with common bot commands
- **Discord-Only Mode** ([discord_only.py](discord_only.py)) - Pure Discord commands without external APIs
- **OpenAI Integration** ([openai_only.py](openai_only.py)) - AI-powered features using OpenAI's API

## Setup

### Prerequisites

- Python 3.8 or higher
- Discord account and Discord Developer Portal access
- OpenAI API key (optional, only for AI features)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd discord_bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Copy [.env](.env) and add your credentials:
     - `DISCORD_TOKEN`: Your Discord bot token
     - `DISCORD_CLIENT_ID`: Your application's client ID
     - `OPENAI_API_KEY`: Your OpenAI API key (if using AI features)

### Creating a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Navigate to the "Bot" section
4. Click "Add Bot"
5. Copy the token and add it to your [.env](.env) file
6. Enable necessary intents under "Privileged Gateway Intents":
   - Message Content Intent
   - Server Members Intent (if needed)

### Inviting the Bot

Use this URL format (replace YOUR_CLIENT_ID with your actual client ID):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot
```

## Usage

### Run the main bot:
```bash
python bot.py
```

### Run Discord-only version:
```bash
python discord_only.py
```

### Run OpenAI-integrated version:
```bash
python openai_only.py
```

## Available Commands

### Basic Commands ([bot.py](bot.py))
- `!ping` - Check bot latency
- `!hello` - Get a greeting
- `!info` - Display bot information
- `!help` - Show all available commands

### Discord-Only Commands ([discord_only.py](discord_only.py))
- `!echo <message>` - Repeat your message
- `!userinfo [@user]` - Display user information
- `!serverinfo` - Display server information
- `!poll <question> <option1> <option2> ...` - Create a poll
- `!clear <amount>` - Clear messages (requires Manage Messages permission)

### OpenAI Commands ([openai_only.py](openai_only.py))
- `!ask <question>` - Ask the AI assistant a question
- `!reset` - Reset your conversation history
- `!imagine <prompt>` - Generate an image with DALL-E
- `!summarize <text>` - Summarize the provided text

## Project Structure

```
discord_bot/
├── bot.py              # Main bot implementation
├── discord_only.py     # Discord-native features only
├── openai_only.py      # OpenAI-integrated features
├── .env                # Environment variables (not in git)
├── .gitignore          # Git ignore file
├── discord_notes.txt   # Development notes and tips
├── LICENSE             # MIT License
├── Procfile            # Heroku deployment configuration
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## Deployment

### Heroku Deployment

1. Create a Heroku account and install Heroku CLI
2. Login to Heroku:
```bash
heroku login
```

3. Create a new Heroku app:
```bash
heroku create your-bot-name
```

4. Set environment variables:
```bash
heroku config:set DISCORD_TOKEN=your_token_here
heroku config:set OPENAI_API_KEY=your_api_key_here
```

5. Deploy:
```bash
git push heroku main
```

6. Scale the worker:
```bash
heroku ps:scale worker=1
```

## Development Notes

See [discord_notes.txt](discord_notes.txt) for detailed development tips, common issues, and useful resources.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Check [discord_notes.txt](discord_notes.txt) for common problems
- Review [discord.py documentation](https://discordpy.readthedocs.io/)
- Check Discord API status at [Discord Status](https://discordstatus.com/)

## Acknowledgments

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- OpenAI integration using [OpenAI Python SDK](https://github.com/openai/openai-python)
