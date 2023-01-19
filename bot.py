import asyncio
import datetime
import json
import random
from re import search
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from dotenv import load_dotenv
import os
from loggingChannel import sendLog
from minecraftrcon import ping_MC_server_interaction
from react import checkReact
from prompts import checkForPrompts
from bot_commands import checkForCommands
import member_data
from fileManager import sendImage, sendImageNew
from slash_commands import sendGifNew

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
apikey = os.getenv('TENOR_API_KEY')

intents = discord.Intents(messages=True, guilds=True, guild_messages=True, guild_reactions=True, members=True, reactions=True, presences=True)
intents.message_content = True
intents.reactions = True


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        # Get the guild object
        guild_ids = [786690956514426910,
                     254779349352448001, 885595844999532624]

        for guild_id in guild_ids:
            await tree.sync(guild=client.get_guild(guild_id))
        print("Synced trees")

        # Loaded
        print(await sendLog(log=(f'{client.user} has connected to Discord!'), client=client))
        await updateStatus()

    async def on_message(self, message):
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
        print(
            f'{message.author.name} [{message.author.id}] sent: {message.content} on Channel: {channel.id}')

        # Check if message should be simplified for Minecraft
        if channel.id == 779436910841954354 or channel.id == 779553090097250307:
            print("Message will be simplified.")
            simplify = True

        # Store Mentions if Any
        mentions = message.mentions

        # React to message if appropriate
        await checkReact(message, client)

        # Respond to Prompts
        await checkForPrompts(message, client)


client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
myid = '<@735550470675759106>'


@tree.command(description="Ask me to send a selfie")
async def selfie(interaction: discord.Interaction):
    DIR = './images/selfies/'
    options = len([name for name in os.listdir(
        DIR) if os.path.isfile(os.path.join(DIR, name))])
    selfieNum = random.randint(0, (options - 1))
    print(await sendLog(
        log=f'{interaction.user.name} has asked for a selfie. Sending -> #{selfieNum}!',
        client=client))
    await sendImageNew(interaction, client, "selfie_", selfieNum, DIR)


@tree.command(description="Punch someone")
@app_commands.describe(member='The member to punch')
async def punch(interaction: discord.Interaction, member: discord.Member):
    if member.id == 786698404927504385:
        embed = discord.Embed(title=f"Punching {interaction.user.name}", colour=discord.Colour(0xff0000),
                              description=f"Rest in peace {interaction.user.mention}. You better not try to hurt her again...")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_author(name="Steve from Accounting",
                         icon_url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot/blob/master/images/punch_icon.png?raw=true")
        searchTerm = "anime punch"
    else:
        embed = discord.Embed(title=f"Punching {member.name}", colour=discord.Colour(0xff0000),
                              description=f"Rest in peace {member.mention}")
        embed.set_thumbnail(url=member.display_avatar.url)
        rng = random.randint(1, 2)
        if rng == 2:
            searchTerm = "punch"
        else:
            searchTerm = "anime punch"
        embed.set_author(name="Steve from Accounting",
                         icon_url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot/blob/master/images/punch_icon.png?raw=true")
    await interaction.response.send_message(embed=embed)
    await sendGifNew(interaction, client, searchTerm, random=False)


# Currently Broken
'''
@tree.command(description="Get minecraft server status")
async def mcinfo(interaction: discord.Interaction):
    embed = await ping_MC_server_interaction(client, interaction)
    try:
        await interaction.response.send_message(embed=embed)
    except:
        await interaction.response.send_message("Unable to get server status.")
'''
    


async def updateStatus():
    global streamers
    with open('status.json') as fs:
        data = json.load(fs)
    await client.change_presence(
        activity=await activityType(data))
    # streamers = await checkTwitch(streamers, client)


async def activityType(data):
    if data["activity"]["type"] == "PLAYING":
        return discord.Activity(type=discord.Game(data["activity"]["name"]))
    elif data["activity"]["type"] == "STREAMING":
        return discord.Activity(activity=discord.Streaming(name=data["activity"]["name"], url=data["activity"]["url"]))
    elif data["activity"]["type"] == "WATCHING":
        return discord.Activity(type=discord.ActivityType.watching, name=data["activity"]["name"])
    elif data["activity"]["type"] == "LISTENING":
        return discord.Activity(type=discord.ActivityType.listening, name=data["activity"]["name"])

# Get the TOKEN variable from the environment

client.run(TOKEN)
