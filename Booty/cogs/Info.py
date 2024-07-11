import nextcord
from nextcord.ext import commands
from datetime import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow()

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @commands.command(brief="Show the avatar of a user.")
    async def avatar(self, ctx, *, member: nextcord.Member = None):
        member = member or ctx.author
        embed = nextcord.Embed(title=f"{member.name}'s Avatar")
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(brief="Check the bot's latency.")
    async def ping(self, ctx):
        embed = nextcord.Embed(title="Pong!", description=f"Latency: {round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embed)

    @commands.command(brief="Display detailed information about a user.")
    async def userinfo(self, ctx, *, member: nextcord.Member = None):
        member = member or ctx.author
        roles = [role.mention for role in member.roles]
        embed = nextcord.Embed(title=f"User Info - {member.name}", color=member.color)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Nickname", value=member.display_name)
        embed.add_field(name="Created at", value=member.created_at.strftime("%d/%m/%Y, %H:%M:%S"))
        embed.add_field(name="Joined at", value=member.joined_at.strftime("%d/%m/%Y, %H:%M:%S"))
        embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles", inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Device", value=member.mobile_status, inline=True)
        embed.add_field(name="Web Status", value=member.web_status, inline=True)
        await ctx.send(embed=embed)

    @commands.command(brief="Display the bot's uptime.")
    async def uptime(self, ctx):
        now = datetime.utcnow()
        uptime_delta = now - self.start_time
        hours, remainder = divmod(int(uptime_delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = nextcord.Embed(
            title="Bot Uptime",
            description=f"Bot has been online for: {hours} hours, {minutes} minutes, {seconds} seconds",
            color=nextcord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(brief="Create a poll for the community.")
    async def poll(self, ctx, *, question):
        embed = nextcord.Embed(title="Poll", description=question, color=nextcord.Color.blurple())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @commands.command(brief="Purge a specified number of messages.")
    async def purge(self, ctx, amount: int):
        if amount <= 0:
            await ctx.send("Please provide a valid positive number for the amount of messages to purge.")
            return

        try:
            deleted = await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Successfully purged {len(deleted) - 1} messages.")
        except nextcord.Forbidden:
            await ctx.send("I don't have the necessary permissions to purge messages.")
        except nextcord.HTTPException:
            await ctx.send("Failed to purge messages. An error occurred.")

def setup(bot):
    bot.add_cog(Info(bot))
