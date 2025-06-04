import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Get token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("No token found. Please set DISCORD_TOKEN in .env file") 