import discord
from discord.ext import commands
import datetime
import pytz
import io
import aiohttp
import os
from dotenv import load_dotenv
import json
import traceback

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='..', intents=intents)

# Dictionary to store server logging channels
# Format: {server_id: logging_channel_id}
SERVER_LOGGING_CHANNELS = {}

def load_server_channels():
    try:
        with open('server_channels.json', 'r') as f:
            data = json.load(f)
            # Convert string IDs to integers
            return {int(k): int(v) for k, v in data.items()}
    except FileNotFoundError:
        print("server_channels.json not found. Creating new file...")
        return {}
    except json.JSONDecodeError:
        print("Error reading server_channels.json. Creating new file...")
        return {}
    except Exception as e:
        print(f"Error loading server channels: {e}")
        return {}

def save_server_channels():
    try:
        # Convert integer IDs to strings for JSON storage
        data = {str(k): str(v) for k, v in SERVER_LOGGING_CHANNELS.items()}
        with open('server_channels.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving server channels: {e}")

# Load saved server channels
SERVER_LOGGING_CHANNELS = load_server_channels()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print("\nConnected to servers:")
    for guild in client.guilds:
        print(f"- {guild.name} (ID: {guild.id})")
        if guild.id not in SERVER_LOGGING_CHANNELS:
            print(f"  Warning: No logging channel set for this server!")
        else:
            channel = client.get_channel(SERVER_LOGGING_CHANNELS[guild.id])
            if channel:
                print(f"  Logging channel: #{channel.name}")
            else:
                print(f"  Error: Logging channel {SERVER_LOGGING_CHANNELS[guild.id]} not found!")

@client.event
async def on_error(event, *args, **kwargs):
    print(f"Error in {event}:")
    traceback.print_exc()

@client.command()
@commands.has_permissions(administrator=True)
async def setlog(ctx, channel: discord.TextChannel = None):
    """Set the logging channel for this server"""
    try:
        # If no channel is specified, use the current channel
        if channel is None:
            channel = ctx.channel

        # Check if the bot has permission to send messages in the channel
        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("❌ I don't have permission to send messages in that channel!")
            return

        # Check if the bot has permission to read message history
        if not channel.permissions_for(ctx.guild.me).read_message_history:
            await ctx.send("❌ I don't have permission to read message history in that channel!")
            return

        # Set the logging channel
        SERVER_LOGGING_CHANNELS[ctx.guild.id] = channel.id
        save_server_channels()

        # Send confirmation message
        embed = discord.Embed(
            title="✅ Logging Channel Set",
            description=f"Logging channel has been set to {channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Server", value=ctx.guild.name, inline=True)
        embed.add_field(name="Channel", value=channel.name, inline=True)
        await ctx.send(embed=embed)

        # Send a test message to the logging channel
        test_embed = discord.Embed(
            title="Test Message",
            description="This is a test message to confirm the logging channel is working.",
            color=discord.Color.blue()
        )
        await channel.send(embed=test_embed)

    except Exception as e:
        print(f"Error in setlog command: {e}")
        traceback.print_exc()
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while setting the logging channel: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)

@client.command()
@commands.has_permissions(administrator=True)
async def removelog(ctx):
    """Remove the logging channel for this server"""
    try:
        if ctx.guild.id in SERVER_LOGGING_CHANNELS:
            del SERVER_LOGGING_CHANNELS[ctx.guild.id]
            save_server_channels()
            embed = discord.Embed(
                title="✅ Logging Channel Removed",
                description="Logging channel has been removed for this server.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="ℹ️ No Logging Channel",
                description="No logging channel was set for this server.",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error in removelog command: {e}")
        traceback.print_exc()
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while removing the logging channel: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)

@client.event
async def on_message(message):
    try:
        # Only process commands, don't log messages
        await client.process_commands(message)
    except Exception as e:
        print(f"Error processing message: {e}")
        traceback.print_exc()

@client.event
async def on_message_delete(message):
    try:
        if message.author == client.user:
            return
            
        # Get logging channel for this server
        if message.guild.id not in SERVER_LOGGING_CHANNELS:
            return  # Skip if no logging channel set for this server
            
        channel = client.get_channel(SERVER_LOGGING_CHANNELS[message.guild.id])
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

@client.event
async def on_message_edit(before, after):
    try:
        if before.author == client.user:
            return
            
        if before.content == after.content:
            return
            
        # Get logging channel for this server
        if before.guild.id not in SERVER_LOGGING_CHANNELS:
            return  # Skip if no logging channel set for this server
            
        channel = client.get_channel(SERVER_LOGGING_CHANNELS[before.guild.id])
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

# Get token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("No token found. Please set DISCORD_TOKEN in .env file")

client.run(TOKEN)
