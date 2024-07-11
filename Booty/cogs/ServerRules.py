import nextcord
from nextcord.ext import commands

class ServerRules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Display the server rules.")
    async def serverrules(self, ctx):
        # Replace with your rules channel ID
        rules_channel_id = 1132770950610440383

        # Get the rules channel
        rules_channel = ctx.guild.get_channel(rules_channel_id)

        if not rules_channel:
            await ctx.send("Rules channel not found. Please ensure the channel ID is correct.")
            return

        # Fetch the messages from the rules channel
        async for message in rules_channel.history(limit=1):
            # Check if the message is an embed
            if message.embeds:
                # If the message is an embed, simply resend it
                embed = message.embeds[0]
                await ctx.send(embed=embed)
            else:
                # If the message is not an embed, create a new embed with the message content
                embed = nextcord.Embed(
                    title="Server Rules",
                    description=message.content,
                    color=nextcord.Color.green()
                )
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ServerRules(bot))
