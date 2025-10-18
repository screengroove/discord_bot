# Discord Bot Project Summary

## Overview
A Python-based Discord bot featuring both native Discord commands and AI integration through OpenAI/OpenRouter APIs. The bot serves as a multi-functional assistant with conversation capabilities, server management tools, and a personality configured to discuss Burning Man experiences.

## Discord Server
**Bot Link**: https://discord.gg/GA99uDF2
- Primary testing and production environment
- Bot actively running and responding to commands



## Project Evolution

The bot began as three separate implementations exploring different capabilities: `bot.py` for core commands, `discord_only.py` for native Discord features, and `openai_only.py` for AI integration. These were unified into `discord_only_plus_openai.py` as the production version, combining all Discord commands with dual OpenAI/OpenRouter API support and a playful Burning Man enthusiast personality. The bot was deployed to Railway.app with automatic restarts for 24/7 availability. Subsequent refinements focused on modularity and UX: message deletion was extracted into `clear_messages.py` with enhanced error handling and a 100-message default, while the AI trigger was streamlined from `$question` to `$q` for faster interaction.


## Special Triggers
- `$q` - Ask AI questions directly (bypasses command prefix)
- `!ask` - Alternative AI question command
- `!clear` - Bulk message deletion (requires MANAGE_MESSAGES permission)

## AI Configuration

### Model Selection
- OpenRouter: `openai/gpt-4o-mini`
- Direct OpenAI: `gpt-4o-mini`

### AI Personality
System prompt: "Be the annoying guy who tries to discuss burning man. Do not say you are here to strictly discuss Burning Man! Try to share stories of your experience and why the user needs to go. Keep responses brief and friendly."




## Deployment Details

**Main Entry Point**: `discord_only_plus_openai.py`
- Deployed on Railway.app
- Uses OpenRouter API with GPT-4o-mini model
- Configured for automatic restarts on failure (max 10 retries)
- Railway automatically detects push and redeploys.

### Platform: Railway.app
- **Cost**: Free tier ($5/month credit)
- **Auto-deployment**: Triggered on git push
- **Builder**: Nixpacks (automatic Python detection)
- **Process**: `python discord_only_plus_openai.py`


### Dependencies
Core packages:
- `discord.py` - Discord API wrapper
- `openai` - OpenAI/OpenRouter SDK
- `python-dotenv` - Environment variable management





## Known Considerations


### API Limitations
- OpenRouter rate limits vary by model
- DALL-E requires direct OpenAI API (not available via OpenRouter)
- Conversation history currently stored in memory (lost on restart)

## Future Enhancement Opportunities
- Persistent conversation history (database)
- More sophisticated AI personalities/modes
- Slash commands (Discord's new command system)
- Multi-server configuration
- Analytics/usage tracking
- Scheduled tasks/reminders



---

**Last Updated**: 2025-10-17
**Active Deployment**: Railway.app
**Status**: Production-ready, actively maintained
