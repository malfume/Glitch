import nextcord
from nextcord.ext import commands
import platform
from datetime import datetime

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_update_time = datetime.utcnow()  # Set the initial last update time

    @commands.command(brief="Display information about the bot.")
    async def botinfo(self, ctx):
        # Get bot information
        bot_name = self.bot.user.name
        bot_id = self.bot.user.id
        bot_owner = await self.bot.application_info()
        bot_owner_name = bot_owner.owner.name
        bot_owner_id = bot_owner.owner.id
        bot_prefix = ctx.prefix
        bot_version = nextcord.__version__
        python_version = platform.python_version()

        # Calculate the time since the last update
        time_since_update = datetime.utcnow() - self.last_update_time

        # Create an embed with bot information
        embed = nextcord.Embed(
            title=f"{bot_name} Information",
            description=f"Hello, I'm {bot_name}, a versatile bot ready to assist you!\n\n"
                        f"Here's a bit about me type !cmd to see all the commands",
            color=nextcord.Color.blue()
        )
        embed.add_field(name="Bot ID", value=bot_id, inline=False)
        embed.add_field(name="Owner", value=f"{bot_owner_name} (ID: {bot_owner_id})", inline=False)
        embed.add_field(name="Prefix", value=bot_prefix, inline=False)
        embed.add_field(name="Version", value=f"Bot: {bot_version}\nPython: {python_version}", inline=False)
        embed.add_field(name="Last Update", value=f"{time_since_update.days} days ago", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar.url)

        await ctx.send(embed=embed)

    @commands.command(hidden=True, brief="Reset the last update time. Owner-only command.")
    @commands.is_owner()  # Only allow the bot owner to trigger this command
    async def update(self, ctx):
        # Command to update the last update time
        self.last_update_time = datetime.utcnow()
        await ctx.send("Last update time has been reset.")

def setup(bot):
    bot.add_cog(BotInfo(bot))
