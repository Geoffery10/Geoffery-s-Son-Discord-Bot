# bot.py
import os

import discord
from discord import user
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv
from re import search
import json
import requests
import datetime
import bot_commands
import slash_commands
from loggingChannel import sendLog
from react import checkReact
from prompts import checkForPrompts
from bot_commands import checkForCommands
import member_data
from twitch import checkTwitch

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
apikey = os.getenv('TENOR_API_KEY')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

myid = '<@735550470675759106>'
lastBirthday = datetime.datetime(2019, 3, 31)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)


guild_ids = [786690956514426910, 254779349352448001] # Put your server ID in this array.


streamers = [{"name": "geoffery10",
              "started_at": '0'},
             {"name": "steelywheelyy",
              "started_at": '0'},
             {"name": "connordavey33",
              "started_at": '0'},
             {"name": "acnor4",
              "started_at": '0'}]


async def updateStatus():
    global streamers
    with open('status.json') as fs:
        data = json.load(fs)
    await client.change_presence(
        activity=await activityType(data))
    streamers = await checkTwitch(streamers, client)


async def activityType(data):
    if data["activity"]["type"] == "PLAYING":
        return discord.Activity(type=discord.Game(data["activity"]["name"]))
    elif data["activity"]["type"] == "STREAMING":
        return discord.Activity(activity=discord.Streaming(name=data["activity"]["name"], url=data["activity"]["url"]))
    elif data["activity"]["type"] == "WATCHING":
        return discord.Activity(type=discord.ActivityType.watching, name=data["activity"]["name"])
    elif data["activity"]["type"] == "LISTENING":
        return discord.Activity(type=discord.ActivityType.listening, name=data["activity"]["name"])


@client.event
async def on_ready():
    # Loaded
    print(await sendLog(log=(f'{client.user} has connected to Discord!'), client=client))

    await updateStatus()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    member_database = await member_data.get_member_data(client)

    new_member = message.author.id

    members = await member_data.search_member_data(member_database, new_member, message.author)

    # Update Status
    await updateStatus()

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
        async with message.channel.typing():
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
        # print(await sendLog(log=(f'Detected a command: {message.content[1:]}'), client=client))
        message.content = message.content[1:]
        await checkForCommands(message, client, member_database)


# ======================================== SLASH COMMANDS ========================================

@slash.slash(name="anime", description="Sends Anime", guild_ids=guild_ids)
async def anime(ctx):
    await slash_commands.anime(ctx, client)


@slash.slash(name="punch", description="Punch another member of the server", options=[
    create_option(
        name="mention",
        description="Mention another user on the server",
        option_type=6,
        required=True
    )
], guild_ids=guild_ids)
async def punch(ctx, mention: user):
    print(mention.id)
    await slash_commands.punch(ctx, client, mention)


@slash.slash(name="selfie", description="I send you a selfie of myself", guild_ids=guild_ids)
async def selfie(ctx):
    await slash_commands.selfie(ctx, client)


@slash.slash(name="nani", description="Google Translate or something...", guild_ids=guild_ids)
async def nani(ctx):
    await ctx.send('何')


@slash.slash(name="wtf", guild_ids=guild_ids)
async def wtf(ctx):
    await ctx.send('Rude!')


@slash.slash(name="mcinfo", description="Info on Geoffery's Minecraft Server if available", guild_ids=guild_ids)
async def mcinfo(ctx):
    # This one is bugged
    await slash_commands.mcinfo(ctx, client)


@slash.slash(name="tpdne", description="Sends you a person that does not exist", guild_ids=guild_ids)
async def tpdne(ctx):
    await slash_commands.tpdne(ctx)


@slash.slash(name="waifu", description="Sends you a waifu that does not exist", guild_ids=guild_ids)
async def waifu(ctx):
    await slash_commands.waifu(ctx)


@slash.slash(name="hot", description="brrrrrrr", guild_ids=guild_ids)
async def hot(ctx):
    file = discord.File("./video/Hot.mp4", filename="hot.mp4")
    await ctx.send(file=file)


@slash.slash(name="sins", description="Sends you the sins of a user", options=[
    create_option(
        name="mention",
        description="Mention another user on the server",
        option_type=6,
        required=True
    )
], guild_ids=guild_ids)
async def sins(ctx, mention: user):
    member_database = await member_data.get_member_data(client)
    await slash_commands.sins(ctx, client, mention, member_database)


@slash.slash(name="fake_id", description="Sends you a fake id so you can escape the government.", guild_ids=guild_ids)
async def fake_id(ctx):
    print(f"Sending fake id")
    await slash_commands.fake_id(ctx)


@slash.slash(name="joke", description="Sends you a joke.", guild_ids=guild_ids)
async def joke(ctx):
    await slash_commands.joke(ctx)


client.run(TOKEN)
