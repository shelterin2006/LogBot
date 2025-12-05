import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print(f"Message deleted: {message.content}")
        # Logic xử lý log của bạn

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content: return
        print(f"Message edited: {before.content} -> {after.content}")
        # Logic xử lý log của bạn

async def setup(bot):
    await bot.add_cog(Events(bot))