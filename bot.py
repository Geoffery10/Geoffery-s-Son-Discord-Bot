# bot.py
import os

import discord
from dotenv import load_dotenv
from re import search
import json
import requests
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
    # Getting IP
    url = "https://api.ipify.org/?format=json"
    ip = "error"
    r = requests.get(url)
    if r.status_code == 200:
        print("IP Response == 200")
        ip = json.loads(r.content)
        print(f'IP: {ip["ip"]}')

    # Loaded
    print(await sendLog(log=(f'{client.user} has connected to Discord!'), client=client))

    with open('status.json') as fs:
        data = json.load(fs)
    # print(await sendLog(log=(f'New status: -n:{data["activity"]["name"]}'), client=client))
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=data["activity"]["name"]))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Update Status
    with open('status.json') as fs:
        data = json.load(fs)
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=data["activity"]["name"]))

    # Remove DiscordSRV formatting
    if (message.author.id == "779431244222955520") and (message.content.includes(" » ") == True):
        message.content = message.content[message.content.index(" » "):]
        print(await sendLog(log=f'Updated message: {message.content}', client=client))

    # Check for Member in members.json
    channel = message.channel
    guild = message.guild
    simply = False  # True if message will be sent to  minecraft

    # Log message
    print(f'{message.author.name} sent: {message.content} on Channel: {channel.id}')

    if channel == "779436910841954354":
        print("Message will be simplified.")
        simplify = True

    mentions = message.mentions


client.run(TOKEN)
