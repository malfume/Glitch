import nextcord
from nextcord.ext import commands

class RoleInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Display information about a specific role.")
    async def roleinfo(self, ctx, *, role: nextcord.Role):
        # Get role information
        role_name = role.name
        role_id = role.id
        role_color = role.color
        member_count = len(role.members)

        # Create an embed with role information
        embed = nextcord.Embed(
            title=f"Role Information - {role_name}",
            color=role_color
        )
        embed.add_field(name="Role ID", value=role_id)
        embed.add_field(name="Color", value=role_color)
        embed.add_field(name="Member Count", value=member_count)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(RoleInfo(bot))
