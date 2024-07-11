import nextcord
from nextcord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        # Check if the user has administrator permissions
        return ctx.author.guild_permissions.administrator

    @commands.command(name="cmd", brief="Shows all commands")
    async def help(self, ctx):
        # Create a dictionary to store commands based on categories
        command_categories = {}

        # Iterate through all commands
        for command in self.bot.commands:
            if not command.hidden:  # Exclude hidden commands
                # Get or create the category for the command
                category = command.cog_name or "Uncategorized"
                if category not in command_categories:
                    command_categories[category] = []

                # Add the command to its category
                command_categories[category].append(command)

        # Create an embed with categorized commands
        embed = nextcord.Embed(
            title="Available Commands",
            description="Here are the commands I understand, categorized:",
            color=nextcord.Color.blurple()  # Customize color if desired
        )

        # Add fields for each category
        for category, commands in command_categories.items():
            command_list = "\n".join([f"**{cmd.name}** - {cmd.brief or '-'}" for cmd in commands])
            embed.add_field(
                name=category,
                value=command_list,
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name="newcommand", brief="Shows new command")
    async def new_command(self, ctx):
        # Example of a newly added command
        await ctx.send("This is a newly added command!")

    @commands.command(brief="Add a scam link to the list of banned links.")
    async def addscamlink(self, ctx, link: str):
        # Your code to add the link to the list of banned links
        await ctx.send(f"Scam link '{link}' has been added to the list.")

    @commands.command(brief="Show the list of scam links.")
    async def scamlinks(self, ctx):
        # Your code to fetch and display the list of scam links
        scam_links = ["example.com", "scam.site", "phishing.org"]  # Example list, replace with your actual list
        scam_links_formatted = "\n".join(scam_links)
        embed = nextcord.Embed(
            title="List of Scam Links",
            description=scam_links_formatted,
            color=nextcord.Color.red()
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
