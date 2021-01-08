# bot.py
import os

import discord
from dotenv import load_dotenv
from re import search
import json
import requests
import datetime
from loggingChannel import sendLog
from react import checkReact
from prompts import checkForPrompts
from commands import checkForCommands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
apikey = os.getenv('TENOR_API_KEY')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

myid = '<@735550470675759106>'
lastBirthday = datetime.datetime(2019, 3, 31)


@client.event
async def on_ready():
    # Loaded
    print(await sendLog(log=(f'{client.user} has connected to Discord!'), client=client))

    with open('status.json') as fs:
        data = json.load(fs)
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name=data["activity"]["name"]))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Update Status
    with open('status.json') as fs:
        data = json.load(fs)
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name=data["activity"]["name"]))

    # Remove DiscordSRV formatting
    if (message.author.id == "779431244222955520") and search("(\s»\s)", message.content.lower()):
        message.content = message.content[message.content.index(" » "):]
        print(await sendLog(log=f'Updated message: {message.content}', client=client))

    # Check for Member in members.json
    channel = message.channel
    guild = message.guild
    simply = False  # True if message will be sent to  minecraft

    # Log message
    print(f'{message.author.name} sent: {message.content} on Channel: {channel.id}')

    # Check if message should be simplified for Minecraft
    if channel.id == 779436910841954354 or channel.id == 779553090097250307:
        print("Message will be simplified.")
        simplify = True

    # Store Mentions if Any
    mentions = message.mentions

    # React to message if appropriate
    await checkReact(message, client)

    # Check if asked to quit
    if len(mentions) > 0:
        if mentions[0].id == 735550470675759106:
            if search("^!quit", message.content.lower()) and message.channel == client.get_channel(789190323326025789):
                await client.logout()

    # React to a birthday
    now = datetime.datetime.now()
    global lastBirthday
    if search("(^|\s)(happy\sb(irth)?(day)?)", message.content.lower()) and lastBirthday.date() < now.date():
        print("Reacting to a birthday")
        file = discord.File("./images/happybirthday.gif", filename="happybirthday.gif")
        await message.channel.send(file=file)
        lastBirthday = now
    if search("(^!birthdayreset)", message.content.lower()) and message.author.id == 253710834553847808:
        lastBirthday = datetime.datetime(2019, 3, 31)
        print(await sendLog(log=(f'Resetting birthday clock to {lastBirthday.date()}.'), client=client))

    # Respond to Prompts
    await checkForPrompts(message, client)

    # Respond to Commands
    if search("(^!\S)", message.content):
        print(await sendLog(log=(f'Detected a command: {message.content[1:]}'), client=client))
        message.content = message.content[1:]
        await checkForCommands(message, client)


client.run(TOKEN)
