import discord
from discord.ext import commands
import os
import traceback
from utils.config import TOKEN
# Giả sử Events class của bạn nằm ở đây
from cogs.events import Events


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
            application_id=None
        )
        # Khởi tạo Events helper tại đây và truyền bot (self) vào
        self.events_helper = Events(self)

    async def setup_hook(self):
        # 1. Load các extension (Cogs)
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Loaded extension: {filename}')
                except Exception as e:
                    print(f'Failed to load extension {filename}. Error: {e}')

        # 2. SYNC GLOBAL (QUAN TRỌNG)
        # Lệnh này sẽ đẩy command lên toàn bộ server bot đang tham gia
        print("Đang bắt đầu Sync Global... (Có thể mất 1 lúc)")
        synced = await self.tree.sync()
        print(f"Đã sync {len(synced)} lệnh Global thành công!")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        # Gọi event từ class Events cũ của bạn
        if hasattr(self.events_helper, 'on_ready'):
            await self.events_helper.on_ready()

    async def on_message_delete(self, message):
        # Gọi event xử lý delete
        if hasattr(self.events_helper, 'on_message_delete'):
            await self.events_helper.on_message_delete(message)

    async def on_message_edit(self, before, after):
        # Gọi event xử lý edit
        if hasattr(self.events_helper, 'on_message_edit'):
            await self.events_helper.on_message_edit(before, after)

    async def on_error(self, event_method, *args, **kwargs):
        print(f"Lỗi trong event {event_method}:")
        traceback.print_exc()
        # Gọi event xử lý error nếu class Events có hỗ trợ
        if hasattr(self.events_helper, 'on_error'):
            await self.events_helper.on_error(event_method, *args, **kwargs)


# Khởi chạy bot
bot = MyBot()
print("Đang khởi động bot...")
bot.run(TOKEN)