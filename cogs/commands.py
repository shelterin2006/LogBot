from discord import app_commands
import discord
import traceback
from utils.config import SERVER_LOGGING_CHANNELS, save_server_channels
print("Đã import cogs/commands.py")
@app_commands.command(name="hello", description="Bot sẽ gửi lời chào.")
@app_commands.guild_only()
async def hello(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(f"Xin chào, {interaction.user.mention}!")
    except Exception as e:
        print(f"Lỗi trong lệnh hello: {e}")
        traceback.print_exc()
        await interaction.response.send_message("Đã xảy ra lỗi khi thực hiện lệnh!", ephemeral=True)

@app_commands.command(name="setlog", description="Set the logging channel for this server (admin only)")
@app_commands.guild_only()
async def setlog(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """Set the logging channel for this server"""
    # Check admin permission
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You must be an administrator to use this command!", ephemeral=True)
        return
    try:
        # If no channel is specified, use the current channel
        if channel is None:
            channel = interaction.channel

        # Check if the bot has permission to send messages in the channel
        if not channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message("❌ I don't have permission to send messages in that channel!", ephemeral=True)
            return

        # Check if the bot has permission to read message history
        if not channel.permissions_for(interaction.guild.me).read_message_history:
            await interaction.response.send_message("❌ I don't have permission to read message history in that channel!", ephemeral=True)
            return

        # Set the logging channel
        SERVER_LOGGING_CHANNELS[interaction.guild.id] = channel.id
        save_server_channels()

        # Send confirmation message
        embed = discord.Embed(
            title="✅ Logging Channel Set",
            description=f"Logging channel has been set to {channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Server", value=interaction.guild.name, inline=True)
        embed.add_field(name="Channel", value=channel.name, inline=True)
        await interaction.response.send_message(embed=embed)

        # Send a test message to the logging channel
        test_embed = discord.Embed(
            title="Test Message",
            description="This is a test message to confirm the logging channel is working.",
            color=discord.Color.blue()
        )
        await channel.send(embed=test_embed)

    except Exception as e:
        print(f"Error in setlog slash command: {e}")
        traceback.print_exc()
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while setting the logging channel: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)

@app_commands.command(name="removelog", description="Remove the logging channel for this server (admin only)")
@app_commands.guild_only()
async def removelog(interaction: discord.Interaction):
    """Remove the logging channel for this server"""
    # Check admin permission
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You must be an administrator to use this command!", ephemeral=True)
        return
    try:
        if interaction.guild.id in SERVER_LOGGING_CHANNELS:
            del SERVER_LOGGING_CHANNELS[interaction.guild.id]
            save_server_channels()
            embed = discord.Embed(
                title="✅ Logging Channel Removed",
                description="Logging channel has been removed for this server.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="ℹ️ No Logging Channel",
                description="No logging channel was set for this server.",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in removelog slash command: {e}")
        traceback.print_exc()
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while removing the logging channel: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True) 
        

        