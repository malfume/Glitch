# cogs/BotManagement.py
import nextcord
from nextcord.ext import commands

class BotManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelisted_bots = [
            515067662028636170,
            1093009502141427712,
            703886990948565003,
            593826875323842590,
            719806770133991434,
            294882584201003009,
            307998818547531777,
            678344927997853742,
            1032724229172510740,
            458276816071950337,
            557628352828014614,
            508391840525975553,
            1152053196307578951,
            536991182035746816,
            204255221017214977,
            1135355148563128421
        ]

    async def is_whitelisted_bot(self, bot_id):
        return bot_id in self.whitelisted_bots

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            if not await self.is_whitelisted_bot(member.id):
                # Unwhitelisted bot detected
                await member.kick(reason="Unwhitelisted bot. Contact the server owner to whitelist.")

                # Send message to server owner
                guild = member.guild
                owner = guild.owner
                await owner.send(f"Unwhitelisted bot '{member.name}' ({member.id}) was kicked. Whitelist it to allow entry.")

    @commands.command()
    async def whitelistbot(self, ctx, bot_id: int):
        """
        Whitelist a bot by providing its ID.
        """
        if bot_id not in self.whitelisted_bots:
            self.whitelisted_bots.append(bot_id)
            await ctx.send(f"Bot with ID {bot_id} has been whitelisted.")
        else:
            await ctx.send(f"Bot with ID {bot_id} is already whitelisted.")

    @commands.command()
    async def listwhitelistedbots(self, ctx):
        """
        List all whitelisted bot IDs.
        """
        if self.whitelisted_bots:
            whitelisted_bots_str = "\n".join(str(bot_id) for bot_id in self.whitelisted_bots)
            await ctx.send(f"Whitelisted Bot IDs:\n{whitelisted_bots_str}")
        else:
            await ctx.send("No bots are whitelisted.")

def setup(bot):
    bot.add_cog(BotManagement(bot))
