import nextcord
from nextcord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        # Check if the user has administrator permissions
        return ctx.author.guild_permissions.administrator

    @commands.command(brief="Display information about the server.")
    async def serverinfo(self, ctx):
        guild = ctx.guild

        # Calculate member count, bot count, and online members
        member_count = guild.member_count
        bot_count = sum(1 for member in guild.members if member.bot)
        online_members = sum(1 for member in guild.members if member.status == nextcord.Status.online)

        # Get server creation date, owner, and region
        creation_date = guild.created_at.strftime("%Y-%m-%d")
        owner = guild.owner
        region = str(guild.region)

        # Create an enhanced embed
        embed = nextcord.Embed(
            title=f"Server Information for {guild.name}",
            description=f"Here is some information about {guild.name}",
            color=nextcord.Color.teal()
        )
        embed.add_field(name="Total Members", value=f"{member_count} members\n({bot_count} bots)", inline=False)
        embed.add_field(name="Online Members", value=f"{online_members} members currently online", inline=False)
        embed.add_field(name="Server Created On", value=creation_date, inline=False)
        embed.add_field(name="Server Owner", value=f"{owner.mention}\n(ID: {owner.id})", inline=False)
        embed.add_field(name="Server Region", value=region, inline=False)
        embed.set_footer(text="Thank you for being a part of our community!")

        # Check if the guild has an icon
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ServerInfo(bot))
