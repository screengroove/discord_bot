import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Bot setup with OpenAI integration
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=os.getenv('BOT_PREFIX', '!'),
    intents=intents
)

# Store conversation history per user
conversation_history = {}


@bot.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="AI Assistant Mode"))


def get_ai_response(user_id: int, prompt: str) -> str:
    """Get a response from OpenAI's API."""
    try:
        # Initialize conversation history for new users
        if user_id not in conversation_history:
            conversation_history[user_id] = [
                {"role": "system", "content": "You are a helpful Discord bot assistant. Keep responses concise and friendly."}
            ]

        # Add user message to history
        conversation_history[user_id].append({"role": "user", "content": prompt})

        # Keep only last 10 messages to avoid token limits
        if len(conversation_history[user_id]) > 11:
            conversation_history[user_id] = [conversation_history[user_id][0]] + conversation_history[user_id][-10:]

        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history[user_id],
            max_tokens=500,
            temperature=0.7
        )

        assistant_message = response.choices[0].message.content

        # Add assistant response to history
        conversation_history[user_id].append({"role": "assistant", "content": assistant_message})

        return assistant_message

    except Exception as e:
        logger.error(f'Error getting AI response: {e}')
        return "Sorry, I encountered an error while processing your request."


@bot.command(name='ask')
async def ask(ctx, *, question: str):
    """Ask the AI assistant a question."""
    async with ctx.typing():
        response = get_ai_response(ctx.author.id, question)

        # Split long responses into multiple messages if needed
        if len(response) > 2000:
            chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(response)


@bot.command(name='reset')
async def reset(ctx):
    """Reset your conversation history with the AI."""
    if ctx.author.id in conversation_history:
        del conversation_history[ctx.author.id]
        await ctx.send("Your conversation history has been reset.")
    else:
        await ctx.send("You don't have any conversation history to reset.")


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
        return

    if not api_key:
        logger.error('OPENAI_API_KEY not found in environment variables')
        return

    try:
        bot.run(token)
    except Exception as e:
        logger.error(f'Error running bot: {e}')


if __name__ == '__main__':
    main()
