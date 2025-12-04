import discord
from discord import app_commands
from utils.config import TOKEN
from cogs.commands import hello, setlog, removelog
from cogs.events import Events
import traceback

# Khởi tạo bot với intents
intents = discord.Intents.default()
intents.message_content = True  # Cần bật Message Content Intent trong Discord Developer Portal
intents.members = True  # Cần bật Server Members Intent trong Discord Developer Portal

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
client.tree = tree  # Cho phép truy cập client.tree ở các module khác

# Khởi tạo các cogs
events = Events(client)

# Đăng ký các commands
try:
    tree.add_command(hello)
except Exception as e:
    print("Lỗi add hello:", e)
tree.add_command(setlog)
tree.add_command(removelog)

@app_commands.command(name="test", description="Test command")
async def test(interaction:discord.Interaction):
    await interaction.response.send_message("Test thành công!")

tree.add_command(test)

print("Commands trong tree sau khi add:", [cmd.name for cmd in tree.get_commands()])

# Đăng ký các event handlers
GUILD_IDS = [1008728257253867621]  # Thay bằng các guild ID của bạn

@client.event
async def on_ready():
    print(f'Bot đã đăng nhập với tên {client.user}')
    print(f'Bot ID: {client.user.id}')
    print('Đang xóa và sync commands...')
    try:
        # 1. Xóa và sync từng guild
        print("Commands trong tree:", [cmd.name for cmd in tree.get_commands()])
        for gid in GUILD_IDS:
            guild = discord.Object(id=gid)
            tree.clear_commands(guild=guild)
            
            print(f"Đã xóa commands cho guild {gid}")
            synced = await tree.sync(guild=None)
            print(f"Đã sync {len(synced)} commands cho guild {gid}")
            for cmd in synced:
                print(f"- /{cmd.name}")
    except Exception as e:
        print(f"Lỗi khi sync commands: {e}")
        traceback.print_exc()
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
