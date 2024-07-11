import nextcord
from nextcord.ext import commands
import os
import asyncio
import aiohttp
from datetime import datetime
import json
from config import Token

# Define bot intents
intents = nextcord.Intents.all()
intents.members = True

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# ID of the server and the channel where you want to log messages
LOG_SERVER_ID = 1138266674332717096  # Replace with your server ID
LOG_CHANNEL_ID = 1140885101861933138  # Replace with your channel ID

# Define a class for the Verification cog
class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_scam_links()
        self.link_logs_channel_id = 1233482087898546207  # Replace with the ID of the channel to log links

    def load_scam_links(self):
        try:
            with open("Scamlinks.json", "r") as f:
                self.scam_links = json.load(f)
        except FileNotFoundError:
            self.scam_links = []

    def save_scam_links(self):
        with open("Scamlinks.json", "w") as f:
            json.dump(self.scam_links, f)

    async def cog_check(self, ctx):
        # Check if the user has administrator permissions
        return ctx.author.guild_permissions.administrator

    async def mute_user(self, member):
        muted_role = nextcord.utils.get(member.guild.roles, name="Quarantine")  # Replace with the actual muted role name

        if not muted_role:
            return False  # Muted role not found

        try:
            await member.add_roles(muted_role)
            return True  # User successfully muted
        except nextcord.Forbidden:
            return False  # Bot does not have permissions to add roles

    async def check_scam_links(self, message):
        for link in self.scam_links:
            if link in message.content:
                return True
        return False

    async def log_links(self, message):
        link_logs_channel = self.bot.get_channel(self.link_logs_channel_id)
        if link_logs_channel:
            if message.content:
                for word in message.content.split():
                    if word.startswith("http://") or word.startswith("https://"):
                        await link_logs_channel.send(f"Link sent by {message.author.mention}: {word}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:  # Check if message author is the bot to prevent infinite loops
            return

        # Check for mentions of @everyone or @here
        if any(role.mention in message.content for role in message.role_mentions):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, mentioning @everyone or @here is not allowed.")
            # Timeout the user for 7 days
            try:
                await message.author.add_roles(verified_role)  # Assuming you have a role named 'verified_role'
                await asyncio.sleep(7 * 24 * 60 * 60)  # Timeout for 7 days
                await message.author.remove_roles(verified_role)  # Remove the role after timeout
            except nextcord.Forbidden:
                print("Bot does not have permissions to add or remove roles.")

        await self.log_links(message)

        for guild in self.bot.guilds:
            log_channel = nextcord.utils.get(guild.channels, id=LOG_CHANNEL_ID)
            if log_channel:
                embed = nextcord.Embed(title="Message Log", color=0x00ff00)
                embed.add_field(name="Author", value=message.author.mention, inline=False)
                embed.add_field(name="Channel", value=message.channel.mention, inline=False)
                embed.add_field(name="Content", value=message.content, inline=False)
                embed.add_field(name="Date and Time", value=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), inline=False)
                if message.attachments:
                    files = [attachment.url for attachment in message.attachments]
                    embed.add_field(name="Files", value='\n'.join(files), inline=False)
                await log_channel.send(embed=embed)

                # Check for scam links
                if await self.check_scam_links(message):
                    await message.delete()
                    await log_channel.send(f"Scam link detected and message deleted: {message.content}")
                    # Mute the user
                    if await self.mute_user(message.author):
                        await log_channel.send(f"{message.author.mention} has been muted for sending a scam link.")
                    else:
                        await log_channel.send(f"Failed to mute {message.author.mention}.")

        await self.bot.process_commands(message)

    @commands.command(brief="Add a scam link to the blacklist.")
    async def add_scam_link(self, ctx, link: str):
        """Add a scam link to the blacklist."""
        self.scam_links.append(link)
        self.save_scam_links()
        await ctx.send(f"Scam link '{link}' has been added to the blacklist.")

    @commands.command(brief="Remove a scam link from the blacklist.")
    async def remove_scam_link(self, ctx, link: str):
        """Remove a scam link from the blacklist."""
        if link in self.scam_links:
            self.scam_links.remove(link)
            self.save_scam_links()
            await ctx.send(f"Scam link '{link}' has been removed from the blacklist.")
        else:
            await ctx.send(f"Scam link '{link}' not found in the blacklist.")

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('_______________________________________________')

    # Set bot status
    statuses = [
        nextcord.Activity(type=nextcord.ActivityType.streaming, name="Drowned Hub", url="https://www.twitch.tv/your_stream_url"),
        nextcord.Activity(type=nextcord.ActivityType.listening, name="user requests"),
        nextcord.Activity(type=nextcord.ActivityType.watching, name="server activities")
    ]
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.playing, name="Setting up..."))
    await asyncio.sleep(5)
    await bot.change_presence(activity=statuses[0], status=nextcord.Status.online)

    # Load Cogs (including Verification)
    loaded_cogs = set()
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = f'cogs.{filename[:-3]}'
            print(f"Attempting to load cog: {cog_name}")
            try:
                bot.load_extension(cog_name)
                loaded_cogs.add(cog_name)
                print(f"Cog {cog_name} loaded successfully.")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Failed to load cog {cog_name}. Error: {e}")

    # Perform automatic verification
    await automatic_verification()

# Automatic verification function
async def automatic_verification():
    print("Performing automatic verification...")
    guild_id = 1112286237710098483
    channel_id = 1117181841187799181
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id) if guild else None

    if not channel:
        print(f"Channel with ID {channel_id} not found. Please ensure it exists.")
        return

    verified_role_name = "Verified"
    unverified_role_name = "unverified"

    verified_role = nextcord.utils.get(guild.roles, name=verified_role_name)
    unverified_role = nextcord.utils.get(guild.roles, name=unverified_role_name)

    if not verified_role or not unverified_role:
        print(f"Roles '{verified_role_name}' or '{unverified_role_name}' not found. Please ensure they exist.")
        return

    for member in guild.members:
        if verified_role in member.roles and unverified_role in member.roles:
            try:
                await member.remove_roles(unverified_role)
                await channel.send(f"Removed '{unverified_role_name}' role from {member.mention}")
                print(f"Removed '{unverified_role_name}' role from {member.display_name}")
            except nextcord.Forbidden:
                print(f"Bot does not have permissions to remove roles from {member.display_name}")

    await channel.send(f"Unverification completed. Members with the '{verified_role_name}' role have been unverified.")
    print(f"Unverification completed. Members with the '{verified_role_name}' role have been unverified.")

# Command to check and kick unauthorized bots
@bot.command()
async def check_bots(ctx):
    """Check if bots in the server are whitelisted and kick if not."""
    whitelisted_bot_ids = [515067662028636170, 1093009502141427712, 703886990948565003, 593826875323842590, 1171712670823612428,
                           719806770133991434, 294882584201003009, 307998818547531777, 678344927997853742, 
                           1032724229172510740, 458276816071950337, 557628352828014614, 508391840525975553, 
                           115205319630757821, 536991182035746816, 204255221017214977, 1135355148563128421]

    for member in ctx.guild.members:
        if member.bot and member.id not in whitelisted_bot_ids:
            try:
                await member.kick(reason="Not whitelisted.")
                await ctx.send(f"Kicked {member.name} ({member.id}) because it's not whitelisted.")
            except nextcord.Forbidden:
                await ctx.send(f"Bot does not have permissions to kick {member.name} ({member.id}).")

# Command to fetch game information
@bot.command()
async def game_info(ctx, game_id: int):
    """Fetch game information from the Roblox API."""
    try:
        url = f"https://games.roblox.com/v1/games/{game_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send("Failed to fetch game information.")
                    return

                game_data = await response.json()
                if "data" not in game_data:
                    await ctx.send("No game information found.")
                    return

                game_info = game_data["data"][0]
                embed = nextcord.Embed(title=game_info["name"], description=game_info["description"], color=0x00ff00)
                embed.add_field(name="Creator", value=game_info["creator"]["name"])
                embed.add_field(name="Visits", value=game_info["visits"])
                embed.add_field(name="Favorites", value=game_info["favorites"])
                embed.add_field(name="Max Players", value=game_info["maxPlayers"])
                embed.add_field(name="Created", value=game_info["created"])
                embed.add_field(name="Updated", value=game_info["updated"])
                embed.add_field(name="Likes", value=game_info["upVotes"])
                embed.add_field(name="Dislikes", value=game_info["downVotes"])
                embed.set_thumbnail(url=game_info["thumbnailUrl"])

                await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Command to get an alt account
@bot.command()
async def get_alt_account(ctx):
    """Get an alternate account."""
    try:
        file_path = "C:\\Users\\lorde\\Downloads\\booty\\cogs\\acc.txt"  # Update to the correct absolute path

        with open(file_path, "r") as file:
            accounts = file.readlines()
        
        if not accounts:
            await ctx.send("No accounts available.")
            return

        # Get a random account or the first one
        account = accounts[0].strip()
        username, password = account.split(":")
        
        embed = nextcord.Embed(title="Alt Account", color=0x00ff00)
        embed.add_field(name="Username", value=username, inline=False)
        embed.add_field(name="Password", value=password, inline=False)
        
        await ctx.send(embed=embed)
        
        # Optionally, remove the account from the file after providing it
        with open(file_path, "w") as file:
            file.writelines(accounts[1:])

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Command to upload and check accounts
@bot.command()
async def upload_accounts(ctx):
    """Upload and check accounts."""
    try:
        if not ctx.message.attachments:
            await ctx.send("No file attached.")
            return

        file = ctx.message.attachments[0]
        if not file.filename.endswith('.txt'):
            await ctx.send("Uploaded file must be a text file (.txt).")
            return

        file_content = await file.read()
        accounts = file_content.decode().splitlines()

        if not accounts:
            await ctx.send("No accounts found in the uploaded file.")
            return

        file_path = "C:\\Users\\lorde\\Downloads\\booty\\cogs\\acc.txt"  # Update to the correct absolute path

        async with aiohttp.ClientSession() as session:
            valid_accounts = []
            for account in accounts:
                parts = account.split(":")
                if len(parts) == 2:
                    username, password = parts
                    if await check_username_exists(session, username):
                        valid_accounts.append(account)

        if not valid_accounts:
            await ctx.send("No valid accounts found.")
            return

        with open(file_path, "a") as file:
            for account in valid_accounts:
                file.write(account + "\n")

        await ctx.send("Valid accounts successfully added.")

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

async def check_username_exists(session, username):
    """Check if a Roblox username exists."""
    try:
        url = f"https://api.roblox.com/users/get-by-username?username={username}"
        async with session.get(url) as response:
            data = await response.json()
            if "Id" in data:
                return True
            return False
    except Exception as e:
        print(f"Error checking username {username}: {e}")
        return False

# Command to create a role and assign to all members
@bot.command()
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, *, role_name: str):
    """Create a role with the specified name and assign it to all members."""
    guild = ctx.guild

    # Check if the role already exists
    role = nextcord.utils.get(guild.roles, name=role_name)
    if role:
        await ctx.send(f"The role '{role_name}' already exists.")
        return

    try:
        # Create the role
        role = await guild.create_role(name=role_name)
        await ctx.send(f"Role '{role_name}' created successfully.")

        # Assign the role to all members
        for member in guild.members:
            if not member.bot:  # Optionally skip bots
                await member.add_roles(role)

        await ctx.send(f"Role '{role_name}' has been assigned to all members.")

    except nextcord.Forbidden:
        await ctx.send("I do not have permission to create roles or assign them.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Run the bot
bot.run(Token)
