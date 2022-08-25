
import discord


client = commands.Bot(command_prefix = '..')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



client.run("OTI0Njc1MjQ4ODcwMjczMDU2.GxcDT1._YQnpHbjxHlWKM5aMiYDujNnC_theL52k0jY0o")
