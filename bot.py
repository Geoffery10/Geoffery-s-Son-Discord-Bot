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
import os.path
from loggingChannel import sendLog
from minecraftrcon import ping_MC_server, ping_MC_server_interaction
from react import checkReact
from prompts import checkForPrompts
import member_data
from fileManager import sendImage, sendImageNew
from slash_commands import sendGifNew, sendGif
import requests
from random import randint, randrange
import russianroulette
from r2loadout import get_r2loadout
from time import sleep

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

        # Log message
        print(
            f'{message.author.name} [{message.author.id}] sent: {message.content} on Channel: {message.channel.id}')

        # React to message if appropriate (keyword emoji reacts)
        await checkReact(message, client)

        # Respond to ambient phrase triggers (sauce, heresy, etc.)
        await checkForPrompts(message, client)


client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
myid = '<@735550470675759106>'

# Slash command guilds (for instant registration; can take up to 1h globally)
SYNC_GUILDS = [786690956514426910, 254779349352448001, 885595844999532624]


# ---------------------------------------------------------------------------
# Slash commands
# ---------------------------------------------------------------------------

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


@tree.command(description="Send a random anime gif")
async def anime(interaction: discord.Interaction):
    localOrOnline = randint(1, 3)
    if localOrOnline >= 2:  # Online
        await sendGifNew(interaction, client, "cute anime girl", random=False)
    else:
        DIR = './images/anime/'
        options = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        animeNum = random.randint(0, (options - 1))
        await sendImageNew(interaction, client, "anime_", animeNum, DIR)


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


@tree.command(description="Roll dice in NdN format (e.g. 3d6)")
@app_commands.describe(
    dice_count="Number of dice to roll",
    dice_sides="Number of sides on each die",
)
async def roll(interaction: discord.Interaction, dice_count: int, dice_sides: int):
    if dice_count < 1 or dice_sides < 1 or dice_count > 100 or dice_sides > 1000:
        await interaction.response.send_message("Please pick reasonable numbers (1-100 dice, 1-1000 sides).")
        return
    value = sum(randint(1, dice_sides) for _ in range(dice_count))
    embed = discord.Embed(
        colour=discord.Colour(0x259944),
        description=f'You rolled {value} on your {dice_count}d{dice_sides}. Good job! At the very least you get an A+ for effort so isn\'t that nice.')
    embed.set_thumbnail(
        url="https://gilkalai.files.wordpress.com/2017/09/dice.png?w=640")
    embed.set_author(name="Steve from Accounting",
                     icon_url="https://www.topaccountingdegrees.org/wp-content/uploads/2015/08/Accounting-7.jpg")
    await interaction.response.send_message(embed=embed)


@tree.command(description="Reveal the sins of a Discord user")
@app_commands.describe(member='Whose sins do you wish to see?')
async def sins(interaction: discord.Interaction, member: discord.Member):
    member_database = await member_data.get_member_data(client)
    sins_found = False
    member_sins = None
    for m in member_database:
        if m['userID'] == member.id:
            sins_found = True
            member_sins = m
            break
    if sins_found:
        embed = discord.Embed(title=f"Sins of {member.display_name}", colour=discord.Colour(0x781dac),
                              description=member_sins['sins'])
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(name="The Devil", url="https://youtu.be/dQw4w9WgXcQ",
                         icon_url="https://i.imgur.com/uLAimaY_d.webp?maxwidth=728&fidelity=grand")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            f"{member.display_name} is sinless... for now... (no entry in the database yet)")


@tree.command(description="Get Minecraft server status")
async def mcinfo(interaction: discord.Interaction):
    embed = await ping_MC_server_interaction(client, interaction)
    try:
        await interaction.response.send_message(embed=embed)
    except Exception:
        await interaction.response.send_message("Unable to get server status.")


@tree.command(description="Ping the bot")
async def ping(interaction: discord.Interaction):
    latency_ms = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! Latency: {latency_ms}ms")


@tree.command(description="Why is this a command?")
async def wtf(interaction: discord.Interaction):
    await interaction.response.send_message('Rude!')


@tree.command(description="It can translate to weeb characters.")
async def nani(interaction: discord.Interaction):
    await interaction.response.send_message('何')


@tree.command(description="AI-generated face that does not exist")
async def thispersondoesnotexist(interaction: discord.Interaction):
    url = "https://fakeface.rest/face/json"
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        await interaction.response.send_message(data['image_url'])
    else:
        await interaction.response.send_message("Failed to load image.")


@tree.command(description="AI-generated waifu that does not exist")
async def waifu(interaction: discord.Interaction):
    url = "https://www.thiswaifudoesnotexist.net/example-"
    num = random.randint(0, 100000)
    await interaction.response.send_message(url + str(num) + ".jpg")


@tree.command(description="Generate a fake ID for a new identity")
async def id(interaction: discord.Interaction):
    url = "https://random-user.p.rapidapi.com/getuser"
    headers = {
        'x-rapidapi-key': os.getenv('X_RAPIDAPI_KEY'),
        'x-rapidapi-host': "random-user.p.rapidapi.com"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = json.loads(r.content)['results'][0]
        embed = discord.Embed(colour=discord.Colour(0xb8b8b8),
                              description=f'ID for {data["name"]["first"]} {data["name"]["last"]}:')
        embed.set_thumbnail(url=data['picture']['large'])
        embed.set_author(name=f'{data["name"]["title"]} {data["name"]["first"]} {data["name"]["last"]}',
                         icon_url=data['picture']['large'], url=data['picture']['large'])
        location = data['location']
        embed.add_field(name="Location",
                        value=f'{location["street"]["number"]} {location["street"]["name"]} {location["city"]}, {location["state"]}, {location["country"]}, {location["postcode"]}')
        embed.add_field(name="Email",
                        value=f'Email: {data["email"]} \nUsername: {data["login"]["username"]} \nPassword: {data["login"]["password"]}')
        embed.add_field(name="Phone Number", value=f'{data["cell"]}')
        embed.add_field(name="Date of Birth",
                        value=f'Age: {data["dob"]["age"]} DOB: {data["dob"]["date"]}')
        if data.get('id', {}).get('value') is not None:
            embed.add_field(name="ID", value=f'Type: {data["id"]["name"]} Value: {data["id"]["value"]}')
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            f"Command failed due to server error {r.status_code}. Please try again later.")


@tree.command(description="BRRRRRRRR!!")
async def hot(interaction: discord.Interaction):
    file = discord.File("./video/Hot.mp4", filename="hot.mp4")
    await interaction.response.send_message(file=file)


@tree.command(description="I'll tell you a joke!")
async def joke(interaction: discord.Interaction):
    await interaction.response.defer()  # joke API calls can be slow
    num = randint(0, 3)
    if num >= 1:
        api_key = os.getenv('JOKE3_RAPIDAPI_KEY')
        if not api_key:
            await interaction.followup.send(
                "Joke API not configured (missing JOKE3_RAPIDAPI_KEY). Falling back...")
        else:
            url = "https://joke3.p.rapidapi.com/v1/joke"
            headers = {
                'x-rapidapi-key': api_key,
                'x-rapidapi-host': "joke3.p.rapidapi.com"
            }
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                joke = json.loads(r.content)
                await interaction.followup.send(joke['content'])
                return
            await interaction.followup.send(
                f"Joke3 API returned {r.status_code}. Falling back to free source...")
    # Fallback (no key required)
    url = "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=racist&type=single"
    r = requests.get(url)
    if r.status_code == 200:
        joke = json.loads(r.content)
        await interaction.followup.send(joke['joke'])
    else:
        await interaction.followup.send("Failed to load joke. Please try again later.")


@tree.command(description="I'll insult you! Be prepared, some of these are pretty terrible...")
async def insult(interaction: discord.Interaction):
    url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        await interaction.response.send_message(data['insult'])
    else:
        await interaction.response.send_message("Failed to load insult. Please try again later.")


@tree.command(description="I'll tell you a random fact.")
async def fact(interaction: discord.Interaction):
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        await interaction.response.send_message(data['text'])
    else:
        await interaction.response.send_message("Failed to load fact. Please try again later.")


@tree.command(description="I'll give you some advice.")
async def advice(interaction: discord.Interaction):
    url = "https://api.adviceslip.com/advice"
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        await interaction.response.send_message(data["slip"]['advice'])
    else:
        await interaction.response.send_message("Failed to load advice. Please try again later.")


@tree.command(description="I'll send a random image of a kitty!")
async def cat(interaction: discord.Interaction):
    cat_api = os.getenv('THE_CAT_API')
    if not cat_api:
        await interaction.response.send_message("Cat API key not configured.")
        return
    url = "https://api.thecatapi.com/v1/images/search?api_key=" + cat_api
    r = requests.get(url)
    if r.status_code == 200:
        cat_data = json.loads(r.content)
        await interaction.response.send_message(cat_data[0]["url"])
    else:
        await interaction.response.send_message("Failed to load cat. Please try again later.")


@tree.command(description="I'll send a random image of a dogo!")
async def dog(interaction: discord.Interaction):
    url = "https://random.dog/woof.json?ref=apilist.fun"
    r = requests.get(url)
    if r.status_code == 200:
        dog_data = json.loads(r.content)
        await interaction.response.send_message(dog_data["url"])
    else:
        await interaction.response.send_message("Failed to load dog. Please try again later.")


@tree.command(description="I'll tell you if the answer is yes or no.")
async def yesorno(interaction: discord.Interaction):
    url = "https://yesno.wtf/api"
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        await interaction.response.send_message(data['image'])
        await interaction.followup.send(data['answer'].capitalize())
    else:
        await interaction.response.send_message("Failed to load answer. Please try again later.")


@tree.command(description="A random load out for a Risk of Rain 2 command run.")
async def r2loadout(interaction: discord.Interaction):
    await interaction.response.send_message(embed=get_r2loadout())


@tree.command(description="Start a game of Russian Roulette")
async def rr(interaction: discord.Interaction):
    await russianroulette.startGame(interaction, client)


@tree.command(description="Pull the trigger in an active Russian Roulette game")
async def shoot(interaction: discord.Interaction):
    await russianroulette.shoot(interaction, client)


@tree.command(description="Spin the cylinder in an active Russian Roulette game")
async def spin(interaction: discord.Interaction):
    await russianroulette.spin(interaction, client)


@tree.command(description="Show this list of commands (sent to your DMs)")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help", colour=discord.Colour(0x9b9b9b), url="https://discordapp.com",
                          description="This is a list of slash commands you can use with Geoffery's Son. Type / to see them all."
                                      "\n\n**OwO**\nConfuses me."
                                      "\n\n**Is it possible to learn this power?**\nNo, leave us..."
                                      "\n\n**The sun is a deadly laser!**\nNot anymore there's a blanket!"
                                      "\n\n**10th/9th time!**\n10th/9th time!"
                                      "\n\n**Sauce**\nThe work of the devil."
                                      "\n\n**Heresy**\nWe must deal with is immediately!"
                                      "\n\n**Ravioli ravioli**\nDragon Loli"
                                      "\n\n**Hentai**\nWait that's illegal!"
                                      "\n\n**Hello there**\nGeneral Kenobi!"
                                      "\n\n**Trap**\nWhat do you think?"
                                      "\n\n**/anime**\nAnime gifs for everyone!"
                                      "\n\n**/roll NdN**\nRolls dice. e.g. /roll dice_count:3 dice_sides:6"
                                      "\n\n**/sins @user**\nInform you of the sins of your friends. I'd watch out for Steve from accounting..."
                                      "\n\n**/punch @user**\nPunch your friends over the internet from a safe distance."
                                      "\n\n**/mcinfo**\nInfo on the Minecraft Server if one is running."
                                      "\n\n**/ping**\nWhat do you expect?"
                                      "\n\n**/wtf**\nWhy is this a command?"
                                      "\n\n**/nani**\nIt can translate to weeb characters."
                                      "\n\n**/thispersondoesnotexist**\nThe smart ai at [thispersondoesnotexist](https://thispersondoesnotexist.com) sends a face that does not exist."
                                      "\n\n**/waifu**\nThe smart ai at [thiswaifudoesnotexist](https://www.thiswaifudoesnotexist.net) sends a waifu that does not exist."
                                      "\n\n**/id**\nCreates your new identity."
                                      "\n\n**/hot**\nBRRRRRRRR!!"
                                      "\n\n**/joke**\nI'll tell you a joke!"
                                      "\n\n**/insult**\nI'll insult you!"
                                      "\n\n**/fact**\nI'll tell you a random fact."
                                      "\n\n**/advice**\nI'll give you some advice."
                                      "\n\n**/cat**\nSends a random kitty!"
                                      "\n\n**/dog**\nSends a random dogo!"
                                      "\n\n**/yesorno**\nTells you if the answer is yes or no."
                                      "\n\n**/r2loadout**\nA random Risk of Rain 2 command run loadout."
                                      "\n\n**/rr**\nStart a game of Russian Roulette."
                                      "\n\n**/shoot**\nPull the trigger."
                                      "\n\n**/spin**\nSpin the cylinder.")
    embed.set_author(name="Geoffery's Son", url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot",
                     icon_url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot/blob/master/images/selfies/selfie_04.png?raw=true")
    # Ephemeral so only the user sees the response
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ---------------------------------------------------------------------------
# Status / startup
# ---------------------------------------------------------------------------

async def updateStatus():
    global streamers
    with open(os.path.join(os.environ.get('BOT_DATA_DIR', '.'), 'status.json')) as fs:
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
