import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
from openai import OpenAI
from clear_messages import setup_clear_command

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client (supports both OpenAI and OpenRouter)
openai_key = os.getenv('OPENAI_API_KEY')
openrouter_key = os.getenv('OPENROUTER_API_KEY')

# Check if OpenAI key is valid (not a placeholder)
if openai_key and openai_key.startswith('sk-') and 'your_' not in openai_key.lower():
    api_key = openai_key
    base_url = None
    logger.info('Using OpenAI API')
# Otherwise use OpenRouter if available
elif openrouter_key:
    api_key = openrouter_key
    base_url = "https://openrouter.ai/api/v1"
    logger.info('Using OpenRouter API')
else:
    api_key = None
    base_url = None
    logger.warning('No valid API key found. AI features will not work.')

if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # List all available models
    try:
        logger.info('Fetching available models...')
        models = client.models.list()

        # Filter for GPT models only
        gpt_models = [model.id for model in models.data if 'gpt' in model.id.lower()]

        if gpt_models:
            logger.info(f'Available GPT models ({len(gpt_models)}):')
            for model in sorted(gpt_models):
                logger.info(f'  - {model}')
        else:
            logger.info('No GPT models found (this is normal for OpenRouter)')
            logger.info('All available models:')
            for model in sorted([m.id for m in models.data])[:10]:  # Show first 10
                logger.info(f'  - {model}')
            if len(models.data) > 10:
                logger.info(f'  ... and {len(models.data) - 10} more models')
    except Exception as e:
        logger.warning(f'Could not fetch models list: {e}')
        logger.info('Bot will continue with default model: gpt-3.5-turbo')
else:
    client = None

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=os.getenv('BOT_PREFIX', '!'),
    intents=intents
)

# Setup clear messages command
setup_clear_command(bot)

# Store conversation history per user
conversation_history = {}


def call_openai(message_content: str) -> str:
    """
    Call OpenAI API with the given message content.

    Args:
        message_content: The user's question or prompt

    Returns:
        The AI's response as a string
    """
    if client is None:
        return "Sorry, the AI service is not configured. Please add OPENAI_API_KEY or OPENROUTER_API_KEY to your .env file."

    try:
        # For OpenRouter, use format: "openai/gpt-4o-mini"
        # For direct OpenAI, use: "gpt-4o-mini"
        model_name = "openai/gpt-4o-mini" if base_url else "gpt-4o-mini"

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", 
                "content": "Be the annoying guy who tries to discuss burning man. Do not say you are here to strictly discuss Burning Man!  Try to share stories of you experience and why the user needs to go. Keep responses brief and friendly."},
                {"role": "user", "content": message_content}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f'Error calling OpenAI API: {e}')
        return f"Sorry, I encountered an error: {str(e)}"


@bot.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')

    await bot.change_presence(
        activity=discord.Game(name="Type $question to ask me anything!")
    )


@bot.event
async def on_message(message):
    """Called when a message is received."""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if message starts with $question
    if message.content.startswith('$question'):
        # Extract the actual question (everything after "$question")
        message_content = message.content.split("$question")[1]

        # Debug print
        print(f"Question: {message_content}")

        # Call OpenAI API
        response = call_openai(message_content)

        # Debug print
        print(f"Assistant: {response}")
        print("------")

        # Send response to Discord channel
        await message.channel.send(response)

    # Process other commands
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


# Discord-only commands (from discord_only.py)

@bot.command(name='ping')
async def ping(ctx):
    """Check if the bot is responsive."""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')


@bot.command(name='hello')
async def hello(ctx):
    """Greet the user."""
    await ctx.send(f'Hello, {ctx.author.mention}!')


@bot.command(name='echo')
async def echo(ctx, *, message: str):
    """Repeat the user's message."""
    await ctx.send(message)


@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member = None):
    """Display information about a user."""
    member = member or ctx.author

    embed = discord.Embed(
        title=f"User Info - {member}",
        color=member.color
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
    embed.add_field(name="Status", value=str(member.status), inline=True)
    embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)

    await ctx.send(embed=embed)


@bot.command(name='serverinfo')
async def serverinfo(ctx):
    """Display information about the server."""
    guild = ctx.guild

    embed = discord.Embed(
        title=f"Server Info - {guild.name}",
        color=discord.Color.green()
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)

    await ctx.send(embed=embed)


@bot.command(name='poll')
async def poll(ctx, question: str, *options):
    """Create a poll with up to 10 options."""
    if len(options) < 2:
        await ctx.send("Please provide at least 2 options.")
        return

    if len(options) > 10:
        await ctx.send("Maximum 10 options allowed.")
        return

    emoji_numbers = ['1�', '2�', '3�', '4�', '5�', '6�', '7�', '8�', '9�', '=']

    description = []
    for i, option in enumerate(options):
        description.append(f"{emoji_numbers[i]} {option}")

    embed = discord.Embed(
        title=question,
        description="\n".join(description),
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Poll by {ctx.author}")

    message = await ctx.send(embed=embed)

    for i in range(len(options)):
        await message.add_reaction(emoji_numbers[i])


# OpenAI-powered commands

@bot.command(name='ask')
async def ask(ctx, *, question: str):
    """Ask the AI assistant a question using !ask command."""
    async with ctx.typing():
        response = call_openai(question)

        # Split long responses into multiple messages if needed
        if len(response) > 2000:
            chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(response)


@bot.command(name='imagine')
async def imagine(ctx, *, prompt: str):
    """Generate an image using DALL-E (requires OpenAI API with DALL-E access)."""
    async with ctx.typing():
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

            image_url = response.data[0].url

            embed = discord.Embed(
                title="Generated Image",
                description=prompt,
                color=discord.Color.purple()
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Requested by {ctx.author}")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f'Error generating image: {e}')
            await ctx.send("Sorry, I couldn't generate the image. Please check your API access and try again.")


@bot.command(name='summarize')
async def summarize(ctx, *, text: str):
    """Summarize the provided text using AI."""
    async with ctx.typing():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                    {"role": "user", "content": f"Summarize this text:\n\n{text}"}
                ],
                max_tokens=300
            )

            summary = response.choices[0].message.content

            embed = discord.Embed(
                title="Summary",
                description=summary,
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f'Error summarizing text: {e}')
            await ctx.send("Sorry, I couldn't summarize the text.")


def main():
    """Main function to run the bot."""
    token = os.getenv('DISCORD_TOKEN')
    api_key = os.getenv('OPENAI_API_KEY')

    if not token:
        logger.error('DISCORD_TOKEN not found in environment variables')
        logger.error(f'DISCORD_TOKEN: {token}')
        return

    if not api_key:
        logger.error('OPENAI_API_KEY not found in environment variables')
        logger.warning('Bot will start but OpenAI features will not work')

    try:
        bot.run(token)
    except discord.LoginFailure:
        logger.error('Invalid token. Please check your DISCORD_TOKEN.')
    except Exception as e:
        logger.error(f'Error running bot: {e}')


if __name__ == '__main__':
    main()
