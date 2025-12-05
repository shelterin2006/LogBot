import discord
from discord import app_commands

from cogs.events import Events
from utils.config import TOKEN
import traceback
from discord.ext import commands
from utils.config import TOKEN
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
events = Events(client)

# Sử dụng commands.Bot thay vì discord.Client
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",  # Prefix cho message command (nếu dùng)
            intents=intents,
            help_command=None,
            application_id=None  # Điền App ID nếu cần thiết
        )

    async def setup_hook(self):
        # Load các extension (Cogs) từ thư mục cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Loaded extension: {filename}')
                except Exception as e:
                    print(f'Failed to load extension {filename}. Error: {e}')

        # Sync command global hoặc guild cụ thể
        # Lưu ý: Sync global mất tới 1 giờ để cập nhật trên mọi server.
        # Sync guild (debug) thì ngay lập tức.

        # Uncomment dòng dưới để sync global (chạy 1 lần rồi comment lại để tránh rate limit)
        # await self.tree.sync()

        # Hoặc sync cho guild cụ thể (Debug nhanh)
        MY_GUILD = discord.Object(id=1008728257253867621)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        print("Commands synced!")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


bot = MyBot()
bot.run(TOKEN)

GUILD_IDS = [1008728257253867621]  # Thay bằng các guild ID của bạn

@client.event
async def on_ready():
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    await events.on_ready()

@client.event
async def on_error(event, *args, **kwargs):
    print(f"Lỗi trong event {event}:")
    traceback.print_exc()
    await events.on_error(event, *args, **kwargs)

@client.event
async def on_message_delete(message):
    await events.on_message_delete(message)

@client.event
async def on_message_edit(before, after):
    await events.on_message_edit(before, after)

# Chạy bot
print("Đang khởi động bot...")
client.run(TOKEN)
