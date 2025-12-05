import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
from datetime import datetime


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Chào bạn!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Xin chào {interaction.user.mention}!")

    @app_commands.command(name="test", description="Test command")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test thành công!")

    @app_commands.command(name="chat", description="Bot sẽ lặp lại tin nhắn bạn gửi trong Embed.")
    @app_commands.describe(message="Tin nhắn bạn muốn bot lặp lại")
    async def chat_command(self, interaction: discord.Interaction, message: str):
        embed = discord.Embed(
            title="💬 Lời nhắn được lặp lại",
            description=f"**Người dùng:** {interaction.user.mention}\n**Nội dung:**\n>>> {message}",
            color=discord.Color.blue()  # Bạn có thể chọn màu khác
        )
        embed.set_footer(text=f"Lệnh được thực thi bởi {interaction.user.display_name}",
                         icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shorturl", description="Tạo link rút gọn")
    @app_commands.describe(url="Link cần rút gọn", custom="Tên tùy chỉnh")
    async def short_url(self, interaction: discord.Interaction, url: str, custom: str = None):
        await interaction.response.defer(thinking=True)
        api_url = "https://shel.id.vn/r/api.php"
        payload = {"url": url}
        if custom:
            payload["custom"] = custom

        async with aiohttp.ClientSession() as session:
            try:
                # Gửi request
                async with session.post(api_url, json=payload) as resp:
                    if resp.status == 200:
                        try:
                            data = await resp.json()

                            # Kiểm tra kết quả trả về (Key 'id' hoặc 'shorturl' tùy API của bạn)
                            if "id" in data or "shorturl" in data:
                                # Lấy link rút gọn
                                short_link = data.get("shorturl", f"https://shel.id.vn/r/{data.get('id', '')}")

                                # --- GIAO DIỆN KẾT QUẢ ---
                                embed = discord.Embed(
                                    title="✅ Rút gọn thành công!",
                                    color=discord.Color.from_rgb(0, 255, 127),  # Màu xanh Spring Green
                                    timestamp=datetime.now()
                                )
                                embed.add_field(name="🔗 Link Gốc", value=f"[{url}]({url})", inline=False)
                                embed.add_field(name="✨ Link Rút Gọn", value=f"**{short_link}**", inline=False)
                                embed.add_field(name="💻 Web online", value=f"https://shel.id.vn/r/", inline=False)

                                # Hiển thị ghi chú nếu là link random hay custom
                                type_text = f"Tùy chỉnh: {custom}" if custom else "Loại: Ngẫu nhiên"
                                embed.set_footer(text=f"{type_text} • Tạo bởi {interaction.user.name}")

                                # Nút mở link nhanh
                                view = discord.ui.View()
                                view.add_item(discord.ui.Button(label="Truy cập ngay", url=short_link,
                                                                style=discord.ButtonStyle.link))

                                await interaction.followup.send(content=f"`{short_link}`",
                                                                embed=embed, view=view)

                            elif "error" in data:
                                await self.send_error(interaction, f"Lỗi từ hệ thống: {data['error']}")
                            else:
                                await self.send_error(interaction, f"Phản hồi không xác định: {data}")

                        except Exception as e:
                            text = await resp.text()
                            await self.send_error(interaction, f"Lỗi đọc dữ liệu: {str(e)}")
                    else:
                        await self.send_error(interaction, f"Lỗi kết nối (HTTP {resp.status})")

            except Exception as e:
                await self.send_error(interaction, f"Lỗi Bot: {str(e)}")

    async def send_error(self, interaction, msg):
        embed = discord.Embed(description=f"❌ **{msg}**", color=discord.Color.red())
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))