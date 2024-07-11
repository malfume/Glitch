import nextcord
from nextcord.ext import commands
import json

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_counter = {}  # Dictionary to store user spam counts
        self.exempted_users = [1111337657822351380, 987654321098765432]  # Replace with actual exempted user IDs
        self.spam_channel_id = 1198319101471363113  # Replace with the actual channel ID
        self.load_scam_links()

    def load_scam_links(self):
        try:
            with open("Scamlinks.json", "r") as file:
                self.scam_links = json.load(file)
        except FileNotFoundError:
            self.scam_links = []

    def save_scam_links(self):
        with open("Scamlinks.json", "w") as file:
            json.dump(self.scam_links, file, indent=4)

    async def delete_user_messages(self, user, spam_channel):
        deleted_messages = []
        async for message in spam_channel.history(limit=None):
            if message.author == user:
                try:
                    await message.delete()
                    deleted_messages.append(message.content)
                except Exception as e:
                    print(f"Error deleting message: {e}")

        # Send a message to the spam channel with the deleted messages
        if deleted_messages:
            deleted_messages_str = "\n".join(deleted_messages)
            await spam_channel.send(f"Deleted messages from user {user.mention}:\n{deleted_messages_str}")

    async def check_spam(self, message, spam_channel):
        user_id = message.author.id

        # Check if the user is exempted
        if user_id in self.exempted_users:
            return

        # Check for repetitive messages
        last_message = getattr(message.author, "last_message", None)
        if last_message and last_message.content == message.content:
            # Increment spam counter for the user
            if user_id not in self.spam_counter:
                self.spam_counter[user_id] = 1
            else:
                self.spam_counter[user_id] += 1

            if self.spam_counter[user_id] >= 5:
                # Ban the user for spamming repetitive messages
                await message.guild.ban(message.author, reason="Spamming repetitive messages")

                # Delete all messages from the user and get the deleted messages
                await self.delete_user_messages(message.author, spam_channel)

                # Reset the spam counter for the banned user
                del self.spam_counter[user_id]

                # Log the ban and message deletion
                print(f"Banned user {message.author} for spamming repetitive messages and deleted their messages")

        # Store the current message for future comparison
        message.author.last_message = message

        # Check for scam links
        if await self.check_scam_links(message):
            await message.delete()
            await spam_channel.send(f"Scam link detected and message deleted: {message.content}")
            # Mute the user
            if await self.mute_user(message.author):
                await spam_channel.send(f"{message.author.mention} has been muted for sending a scam link.")
            else:
                await spam_channel.send(f"Failed to mute {message.author.mention}.")

    async def mute_user(self, member):
        # Implementation of mute_user method goes here (if needed)
        pass

    async def check_scam_links(self, message):
        for link in self.scam_links:
            if link in message.content:
                return True
        return False

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_scam_link(self, ctx, link: str):
        """Add a scam link to the blacklist."""
        if link not in self.scam_links:
            self.scam_links.append(link)
            self.save_scam_links()
            await ctx.send(f"Scam link '{link}' has been added to the blacklist.")
        else:
            await ctx.send(f"Scam link '{link}' is already in the blacklist.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # Ignore messages from bots
            return

        spam_channel = self.bot.get_channel(self.spam_channel_id)

        if message.webhook_id:
            # Perform actions for spam from webhooks (adjust as needed)
            print(f"Webhook message detected: {message.content}")

            # Delete the webhook message
            try:
                await message.delete()
            except Exception as e:
                print(f"Error deleting webhook message: {e}")

            # Send a message to the spam channel about the deleted webhook message
            await spam_channel.send(f"Deleted webhook message in #{message.channel.name}:\n{message.content}")
        else:
            # Check for user messages
            if any(x in message.content.lower() for x in ["discord.gg/", "discord.com/invite/"]):
                await self.check_spam(message, spam_channel)

    @commands.command()
    async def checkspam(self, ctx):
        """
        Checks for spam in all channels of the server.
        """
        spam_channel = self.bot.get_channel(self.spam_channel_id)

        # Iterate over all channels in the server
        for channel in ctx.guild.channels:
            if isinstance(channel, nextcord.TextChannel):
                # Iterate over all messages in the channel and check for spam
                async for message in channel.history(limit=None):
                    await self.check_spam(message, spam_channel)

        await ctx.send("Spam check completed for all channels.")

def setup(bot):
    bot.add_cog(AntiSpam(bot))
