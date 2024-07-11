# ChannelInfo.py
import nextcord
from nextcord.ext import commands

class ChannelInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Display information about the current channel, such as its name, ID, and creation date.")
    async def channelinfo(self, ctx):
        channel = ctx.channel
        channel_name = channel.name
        channel_id = channel.id
        creation_date = channel.created_at.strftime("%d/%m/%Y, %H:%M:%S")

        embed = nextcord.Embed(
            title=f"Channel Information for {channel_name}",
            description=f"ID: {channel_id}\nCreated On: {creation_date}",
            color=nextcord.Color.green()
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ChannelInfo(bot))
