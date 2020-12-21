# bot.py
import os

import discord
from dotenv import load_dotenv
from re import search
from loggingChannel import sendLog

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
apikey = os.getenv('TENOR_API_KEY')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

myid = '<@735550470675759106>'


@client.event
async def on_ready():
    # Loaded
    print(await sendLog(log=(f'{client.user} has connected to Discord!'), client=client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your Health"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    mentions = message.mentions


client.run(TOKEN)
