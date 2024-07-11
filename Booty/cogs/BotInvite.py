# BotInvite.py
import nextcord
from nextcord.ext import commands

class BotInvite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Provide an invite link for users to add the bot to other servers.")
    async def botinvite(self, ctx):
        invite_link = f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=permissions_here"
        await ctx.send(f"Invite me to your server with this link: {invite_link}")

def setup(bot):
    bot.add_cog(BotInvite(bot))
