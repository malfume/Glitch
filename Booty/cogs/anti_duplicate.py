import nextcord
from nextcord.ext import commands

class AntiDuplicate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_count = {}  # Dictionary to store channel creation count
        self.role_count = {}  # Dictionary to store role creation count
        self.duplicate_threshold = 2  # Threshold for considering as duplicate

    async def delete_duplicate(self, entity, name):
        try:
            await entity.delete()
            print(f"Deleted duplicate {type(entity).__name__}: {name}")
        except nextcord.Forbidden:
            print(f"I don't have the necessary permissions to delete {type(entity).__name__}: {name}")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        # Check for duplicate channels
        if channel.id in self.channel_count:
            self.channel_count[channel.id] += 1
            if self.channel_count[channel.id] > self.duplicate_threshold:
                await self.delete_duplicate(channel, channel.name)
        else:
            self.channel_count[channel.id] = 1

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        # Check for duplicate roles
        if role.id in self.role_count:
            self.role_count[role.id] += 1
            if self.role_count[role.id] > self.duplicate_threshold:
                await self.delete_duplicate(role, role.name)
        else:
            self.role_count[role.id] = 1

def setup(bot):
    bot.add_cog(AntiDuplicate(bot))
