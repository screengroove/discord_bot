import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)


def setup_clear_command(bot):
    """
    Set up the clear messages command for the bot.

    Make sure your bot has the "MANAGE_MESSAGES" permission.
    This deletes up to 100 messages (the maximum allowed) that are < 14 days old.
    """

    @bot.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int = 100):
        """Clear messages from the channel (requires Manage Messages permission).

        Usage: !clear [amount]
        - amount: Number of messages to delete (1-100, default: 100)

        Note: Discord only allows bulk deletion of messages less than 14 days old.
        """
        # Validate deleteCount's boundaries
        if amount < 1 or amount > 100:
            await ctx.send("Please provide a number between 1 and 100.")
            return

        try:
            # Bulk delete returns a collection of deleted messages
            # The +1 accounts for the command message itself
            deleted = await ctx.channel.purge(limit=amount + 1, oldest_first=False)

            # Send confirmation message
            confirmation = await ctx.send(f"Deleted {len(deleted) - 1} messages!")

            # Delete confirmation message after 5 seconds
            await confirmation.delete(delay=5)

        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages in this channel!")
        except discord.HTTPException as e:
            logger.error(f'Error deleting messages: {e}')
            await ctx.send("There was an error trying to delete messages in this channel!")
        except Exception as e:
            logger.error(f'Unexpected error in clear command: {e}')
            await ctx.send("An unexpected error occurred while deleting messages.")

    return clear
