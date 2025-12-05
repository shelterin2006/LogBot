import discord
from discord import app_commands
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setlog", description="Cài đặt kênh log")
    @app_commands.default_permissions(administrator=True) # Chỉ admin dùng được
    async def setlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        # Logic setlog của bạn ở đây
        await interaction.response.send_message(f"Đã set log tại {channel.mention}")

    @app_commands.command(name="removelog", description="Xóa kênh log")
    @app_commands.default_permissions(administrator=True)
    async def removelog(self, interaction: discord.Interaction):
        # Logic removelog của bạn ở đây
        await interaction.response.send_message("Đã xóa kênh log.")

async def setup(bot):
    await bot.add_cog(Admin(bot))