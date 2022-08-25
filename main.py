from typing import ClassVar, Sequence
from aiohttp.http import SERVER_SOFTWARE
import discord
from discord import message
from discord import user
from discord import player
from discord import channel
from discord.channel import VoiceChannel
from discord.client import Client
from discord.enums import ExpireBehaviour
from discord.ext import commands
from discord.utils import sleep_until
import time
import io
import aiohttp
import pickle
from datetime import datetime
import pytz
import os

client = commands.Bot(command_prefix = '..')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



client.run("OTI0Njc1MjQ4ODcwMjczMDU2.GxcDT1._YQnpHbjxHlWKM5aMiYDujNnC_theL52k0jY0o")
