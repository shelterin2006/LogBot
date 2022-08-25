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
from a import b
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

@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return
    await client.process_commands(ctx)

res = { 
    952847230648348722 : 952848925226840094, 
    893119319167344700 : 924261082825130026, # arm
      946775239235346492 : 946778374053961738,
      # 897472040511111180 : 918705277098930216 #serve minh
    }
tem = {897472040511111180 : 918705277098930216,
                734325804007161878 : 734325804443631648}
Bot_free = {"Mudae#0807", "Ayana#8911"}
channel_free = {"885546099752968232"}

@client.event
async def on_message_delete(ctx):
    channel = client.get_channel(res[ctx.guild.id])
    if str(ctx.author) not in Bot_free and str(ctx.channel) not in channel_free:
        try:
            ag = content=ctx.attachments[0].url
            a = "```arm" + "\n"
            a += str(ctx.author) + " has delete a File" + "\n"
            a += "File: " + ag[77:len(ag)] + "\n"
            a += "Channel: " + str(ctx.channel) + "\n"
            a += "Time: " + time_string() + "\n"
            a += "This is the file that he has delete!"  + "```"
            # tai anh len discord
            async with aiohttp.ClientSession() as session:
                async with session.get(ag) as resp:
                    data = io.BytesIO(await resp.read())
                    msg = await channel.send(a)
                    await msg.reply(file=discord.File(data, ag[77:len(ag)]))
        except:
            try:
                embeds = ctx.embeds
                msg = await channel.send(embed=embeds[0])
                await msg.reply('This is the embed that ' + str(ctx.author) + 
                ' has delete' + ' in Channel: ' + str(ctx.channel) + ' | Time: ' + time_string())
            except:
              try:
                  a = "```arm" + "\n"
                  a += str(ctx.author) + " has delete a message" + "\n"
                  a += "Message: " + str(ctx.content) + "\n"
                  a += "Channel: " + str(ctx.channel) + "\n"
                  a += "Time: " + time_string() + "\n"
                  a += "This is the message that he has delete!"  + "```"
                  await channel.send(a)
                  b = check_ping(ctx.content)
                  if(b != 0):
                    await ctx.channel.send("<@" + str(ctx.author.id) + ">" +" m thích tag" +  b + "à t xiên giờ ")
                    await ctx.channel.send("?xien")
              except:
                msg = await channel.send(str(ctx.author) + ' has delete ' + ' in Channel: ' + str(ctx.channel) + ' | Time: ' + time_string())
                a = write_file(ctx.content)
                b = check_ping(a)
                if(b != 0):
                  await ctx.channel.send("<@" + str(ctx.author.id) + ">" +" m thích tag" +  b + "à t xiên giờ ")
                  await ctx.channel.send("?xien")
                await msg.reply(file=discord.File("text.txt"))


def check_ping(string):
    string = str(string)
    a = " "
    check = 0
    if(string.find('@everyone',check) != -1): 
        check = string.find('@everyone',check) + 1
        a += "everyone "
    check = 0
    if(string.find('@here',check) != -1):
        check = string.find('@here',check) + 1
        a+= "here "
    if(a == " "):
        return 0
    else:
        return a

@client.event
async def on_message_edit(ctx_bef, ctx_aft):
    channel = client.get_channel(res[ctx_bef.guild.id])
    if str(ctx_bef.author) not in Bot_free and str(ctx_bef.content) != str(ctx_aft.content) and str(ctx_bef.author) not in "ProBot ✨#5803" and str(ctx_bef.author) not in "FredBoat♪♪#7284"  and str(ctx_bef.channel) not in channel_free:
        a = "```arm" + "\n"
        a += str(ctx_bef.author) + " has edit a message" + "\n"
        a += "Old: " + str(ctx_bef.content) + "\n"
        a += "New: " + str(ctx_aft.content) + "\n"
        a += "Channel: " + str(ctx_bef.channel) + "\n"
        a += "Time: " + time_string() + "\n"
        a += "This is the message that he has edit!"  + "```"
        try:
          await channel.send(a)
        except:
          await channel.send(str(ctx_bef.author) + ' has edit ' + 'in ' + time_string())
          await channel.send("```arm" + "\n" + "Old:" + "```")
          write_file(ctx_bef.content)
          await channel.send(file=discord.File("text.txt"))
          await channel.send("```arm" + "\n" + "New:" + "```")
          write_file(ctx_aft.content)
          await channel.send(file=discord.File("text.txt"))
        

def time_string():
    tz_NY = pytz.timezone('Asia/Ho_Chi_Minh')
    datetime_NY = datetime.now(tz_NY)
    return datetime_NY.strftime("%m/%d/%Y, %H:%M:%S")

b()

client.run("OTI0Njc1MjQ4ODcwMjczMDU2.GxcDT1._YQnpHbjxHlWKM5aMiYDujNnC_theL52k0jY0o")
