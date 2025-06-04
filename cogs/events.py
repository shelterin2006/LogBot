import discord
import datetime
import pytz
import io
import aiohttp
import traceback
from utils.config import SERVER_LOGGING_CHANNELS

class Events:
    def __init__(self, client: discord.Client):
        self.client = client

    async def on_ready(self):
        try:
            print(f'We have logged in as {self.client.user}')
            print("\nConnected to servers:")
            for guild in self.client.guilds:
                print(f"- {guild.name} (ID: {guild.id})")
                if guild.id not in SERVER_LOGGING_CHANNELS:
                    print(f"  Warning: No logging channel set for this server!")
                else:
                    channel = self.client.get_channel(SERVER_LOGGING_CHANNELS[guild.id])
                    if channel:
                        print(f"  Logging channel: #{channel.name}")
                    else:
                        print(f"  Error: Logging channel {SERVER_LOGGING_CHANNELS[guild.id]} not found!")
                
        except Exception as e:
            print(f"Error in on_ready: {e}")
            traceback.print_exc()

    async def on_error(self, event, *args, **kwargs):
        print(f"Error in {event}:")
        traceback.print_exc()

    async def on_message_delete(self, message):
        try:
            if message.author == self.client.user:
                return
                
            # Get logging channel for this server
            if message.guild.id not in SERVER_LOGGING_CHANNELS:
                return  # Skip if no logging channel set for this server
                
            channel = self.client.get_channel(SERVER_LOGGING_CHANNELS[message.guild.id])
            if channel is None:
                print(f"Error: Logging channel {SERVER_LOGGING_CHANNELS[message.guild.id]} not found!")
                return
            
            embed = discord.Embed(
                title="Message Deleted",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
            )
            
            embed.add_field(name="Author", value=message.author, inline=True)
            embed.add_field(name="Channel", value=message.channel, inline=True)
            
            # Handle attachments in deleted message
            if message.attachments:
                for attachment in message.attachments:
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                if resp.status == 200:
                                    data = io.BytesIO(await resp.read())
                                    await channel.send(
                                        f"Deleted file from {message.author} in {message.channel}",
                                        file=discord.File(data, attachment.filename)
                                    )
                    except Exception as e:
                        print(f"Error downloading deleted attachment: {e}")
                        traceback.print_exc()
            
            if message.content:
                embed.add_field(name="Content", value=message.content, inline=False)
            
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Error in on_message_delete: {e}")
            traceback.print_exc()

    async def on_message_edit(self, before, after):
        try:
            if before.author == self.client.user:
                return
                
            if before.content == after.content:
                return
                
            # Get logging channel for this server
            if before.guild.id not in SERVER_LOGGING_CHANNELS:
                return  # Skip if no logging channel set for this server
                
            channel = self.client.get_channel(SERVER_LOGGING_CHANNELS[before.guild.id])
            if channel is None:
                print(f"Error: Logging channel {SERVER_LOGGING_CHANNELS[before.guild.id]} not found!")
                return
            
            embed = discord.Embed(
                title="Message Edited",
                color=discord.Color.yellow(),
                timestamp=datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
            )
            
            embed.add_field(name="Author", value=before.author, inline=True)
            embed.add_field(name="Channel", value=before.channel, inline=True)
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            
            # Handle attachments in edited message
            if before.attachments:
                for attachment in before.attachments:
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                if resp.status == 200:
                                    data = io.BytesIO(await resp.read())
                                    await channel.send(
                                        f"Edited file from {before.author} in {before.channel}",
                                        file=discord.File(data, attachment.filename)
                                    )
                    except Exception as e:
                        print(f"Error downloading edited attachment: {e}")
                        traceback.print_exc()
            
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Error in on_message_edit: {e}")
            traceback.print_exc() 