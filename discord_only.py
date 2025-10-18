import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Discord-only bot implementation (without external APIs)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=os.getenv('BOT_PREFIX', '!'),
    intents=intents
)


@bot.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Discord Only Mode"))


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

    emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

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


@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Clear messages from the channel (requires Manage Messages permission)."""
    if amount < 1 or amount > 100:
        await ctx.send("Please specify a number between 1 and 100.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)
    confirmation = await ctx.send(f"Deleted {len(deleted) - 1} messages.")

    # Delete confirmation message after 3 seconds
    await confirmation.delete(delay=3)


def main():
    """Main function to run the bot."""
    token = os.getenv('DISCORD_TOKEN')

    if not token:
        logger.error('DISCORD_TOKEN not found in environment variables')
        return

    try:
        bot.run(token)
    except Exception as e:
        logger.error(f'Error running bot: {e}')


if __name__ == '__main__':
    main()
