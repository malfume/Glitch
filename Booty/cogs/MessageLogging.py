# MessageLogging.py
import nextcord
from nextcord.ext import commands

class MessageLogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Log deleted messages
        log_channel_id = 1197331763769397279  # Replace with your log channel ID
        log_channel = self.bot.get_channel(log_channel_id)

        if log_channel:
            device_type = "Mobile" if message.author.is_on_mobile() else "PC"
            embed = nextcord.Embed(
                title="Message Deleted",
                description=f"**Author:** {message.author.mention} (ID: {message.author.id})\n"
                            f"**Channel:** {message.channel.mention}\n"
                            f"**Content:** {message.content}",
                color=nextcord.Color.red(),
                timestamp=message.created_at
            )

            # Add user profile picture and ID to the embed
            embed.set_thumbnail(url=message.author.avatar.url)

            # Add device information
            embed.add_field(name="Device", value=device_type)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # Log edited messages
        log_channel_id = 123456789012345678  # Replace with your log channel ID
        log_channel = self.bot.get_channel(log_channel_id)

        if log_channel and before.content != after.content:
            device_type = "Mobile" if after.author.is_on_mobile() else "PC"
            embed = nextcord.Embed(
                title="Message Edited",
                description=f"**Author:** {after.author.mention} (ID: {after.author.id})\n"
                            f"**Channel:** {after.channel.mention}\n"
                            f"**Before:** {before.content}\n"
                            f"**After:** {after.content}",
                color=nextcord.Color.orange(),
                timestamp=after.created_at
            )

            # Add user profile picture and ID to the embed
            embed.set_thumbnail(url=after.author.avatar.url)

            # Add device information
            embed.add_field(name="Device", value=device_type)

            await log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(MessageLogging(bot))
