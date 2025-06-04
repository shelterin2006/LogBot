# Discord Message Logger Bot

Bot để log các tin nhắn bị xóa và chỉnh sửa trong Discord server.

## Cài đặt

1. Cài đặt Python 3.8 hoặc cao hơn
2. Cài đặt các thư viện cần thiết:
```bash
pip3 install -r requirements.txt
```

3. Tạo file `.env` với nội dung:
```
DISCORD_TOKEN=your_bot_token_here
```

## Bảo mật

⚠️ **QUAN TRỌNG**: Không bao giờ push các file sau lên GitHub:
- `.env` (chứa token bot)
- `server_channels.json` (chứa cấu hình server)

Các file này đã được thêm vào `.gitignore` để tránh vô tình push lên.

## Cấu hình Bot

1. Tạo bot mới tại [Discord Developer Portal](https://discord.com/developers/applications)
2. Bật các Intents sau trong Discord Developer Portal:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT

3. Mời bot vào server với link sau (thay YOUR_CLIENT_ID bằng Client ID của bot):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot
```

## Quyền cần thiết

Bot cần các quyền sau để hoạt động:

### Quyền cơ bản
- ✅ Send Messages
- ✅ Read Message History
- ✅ View Channels
- ✅ Embed Links
- ✅ Attach Files
- ✅ Read Messages/View Channels

### Quyền cho lệnh admin
- ✅ Administrator (cho lệnh setlog và removelog)

## Cách sử dụng

1. Set channel log:
```
..setlog #channel-name
```
hoặc
```
..setlog
```
(để set channel hiện tại làm channel log)

2. Xóa channel log:
```
..removelog
```

## Tính năng

- Log tin nhắn bị xóa
- Log tin nhắn bị chỉnh sửa
- Log file đính kèm
- Hỗ trợ nhiều server
- Tự động lưu cấu hình
- Thông báo lỗi chi tiết

### Cấu trúc file `server_channels.json`

File này lưu cấu hình kênh log cho từng server. Mỗi server (guild) sẽ có một object với ID là key, value là ID của channel log.

Ví dụ về nội dung file:

```json
{
  "1008728257253867621": 123456789012345678,
  "987654321098765432": 234567890123456789
}
```

- **Key**: Guild ID (ID của server)
- **Value**: Channel ID (ID của kênh log tin nhắn)
