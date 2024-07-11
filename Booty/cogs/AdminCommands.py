# AdminCommands.py
import nextcord
from nextcord.ext import commands

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Delete specified channels.")
    async def delete_channels(self, ctx, *channel_names: str):
        # Check if the user has administrator permissions
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You don't have the necessary permissions to delete channels.")
            return

        # Get all channels in the guild
        for channel in ctx.guild.channels:
            # Check if the channel name is in the provided list and it's not the command channel
            if channel.name.lower() in [name.lower() for name in channel_names] and channel.id != ctx.channel.id:
                try:
                    await channel.delete()
                    await ctx.send(f"Deleted channel: {channel.name}")
                except nextcord.Forbidden:
                    await ctx.send(f"I don't have the necessary permissions to delete {channel.name}")

    @commands.command(brief="Delete specified roles.")
    async def delete_roles(self, ctx, *role_names: str):
        # Check if the user has administrator permissions
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You don't have the necessary permissions to delete roles.")
            return

        # Get all roles in the guild
        for role in ctx.guild.roles:
            # Check if the role name is in the provided list
            if role.name.lower() in [name.lower() for name in role_names]:
                try:
                    await role.delete()
                    await ctx.send(f"Deleted role: {role.name}")
                except nextcord.Forbidden:
                    await ctx.send(f"I don't have the necessary permissions to delete {role.name}")

def setup(bot):
    bot.add_cog(AdminCommands(bot))
