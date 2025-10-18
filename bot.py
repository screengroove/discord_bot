import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=os.getenv('BOT_PREFIX', '!'),
    intents=intents,
    help_command=commands.DefaultHelpCommand()
)


@bot.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')

    # Set bot status
    await bot.change_presence(
        activity=discord.Game(name="Type !help for commands")
    )


@bot.event
async def on_message(message):
    """Called when a message is received."""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Log message for debugging
    logger.debug(f'Message from {message.author}: {message.content}')

    # Process commands
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """Called when a command raises an error."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        logger.error(f'Error in command {ctx.command}: {error}')
        await ctx.send("An error occurred while processing the command.")


@bot.command(name='ping')
async def ping(ctx):
    """Check if the bot is responsive."""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')


@bot.command(name='hello')
async def hello(ctx):
    """Greet the user."""
    await ctx.send(f'Hello, {ctx.author.mention}!')


@bot.command(name='info')
async def info(ctx):
    """Display bot information."""
    embed = discord.Embed(
        title="Bot Information",
        description="A Discord bot with various features",
        color=discord.Color.blue()
    )
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(bot.users), inline=True)
    embed.add_field(name="Prefix", value=bot.command_prefix, inline=True)

    await ctx.send(embed=embed)


def main():
    """Main function to run the bot."""
    token = os.getenv('DISCORD_TOKEN')

    if not token:
        logger.error('DISCORD_TOKEN not found in environment variables')
        return

    try:
        bot.run(token)
    except discord.LoginFailure:
        logger.error('Invalid token. Please check your DISCORD_TOKEN.')
    except Exception as e:
        logger.error(f'Error running bot: {e}')


if __name__ == '__main__':
    main()
