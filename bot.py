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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=data["activity"]["name"]))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    mentions = message.mentions


client.run(TOKEN)
