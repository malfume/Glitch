import nextcord
from nextcord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        # Check if the user has administrator permissions
        return ctx.author.guild_permissions.administrator

    @commands.command(brief="Verify all members with a specified role.")
    async def verifyall(self, ctx):
        verified_role_name = "Verified"  # Replace with the actual role name
        verified_role = nextcord.utils.get(ctx.guild.roles, name=verified_role_name)

        if not verified_role:
            await ctx.send(f"Role '{verified_role_name}' not found. Please ensure it exists.")
            return

        unverified_role_name = "unverified"  # Replace with the actual role name
        unverified_role = nextcord.utils.get(ctx.guild.roles, name=unverified_role_name)

        if not unverified_role:
            await ctx.send(f"Role '{unverified_role_name}' not found. Please ensure it exists.")
            return

        for member in ctx.guild.members:
            if verified_role in member.roles and unverified_role in member.roles:
                try:
                    await member.remove_roles(unverified_role)
                    await ctx.send(f"Removed '{unverified_role_name}' role from {member.mention}")
                except nextcord.Forbidden:
                    await ctx.send(f"Bot does not have permissions to remove roles from {member.mention}")

        await ctx.message.delete()  # Delete message immediately after sending
        await ctx.send(f"All members have been verified with the '{verified_role_name}' role.")

    @commands.command(brief="Remove 'unverified' role from members already verified.")
    async def removeunverify(self, ctx):
        verified_role_name = "Verified"  # Replace with the actual role name
        verified_role = nextcord.utils.get(ctx.guild.roles, name=verified_role_name)

        if not verified_role:
            await ctx.send(f"Role '{verified_role_name}' not found. Please ensure it exists.")
            return

        unverified_role_name = "unverified"  # Replace with the actual role name
        unverified_role = nextcord.utils.get(ctx.guild.roles, name=unverified_role_name)

        if not unverified_role:
            await ctx.send(f"Role '{unverified_role_name}' not found. Please ensure it exists.")
            return

        removed_count = 0
        for member in ctx.guild.members:
            if verified_role in member.roles and unverified_role in member.roles:
                try:
                    await member.remove_roles(unverified_role)
                    removed_count += 1
                    await ctx.send(f"Removed '{unverified_role_name}' role from {member.mention}")
                except nextcord.Forbidden:
                    await ctx.send(f"Bot does not have permissions to remove roles from {member.mention}")

        await ctx.message.delete()  # Delete message immediately after sending
        await ctx.send(f"Unverification completed. {removed_count} members unverified.")

def setup(bot):
    bot.add_cog(Verification(bot))
