import discord
from re import search
import random
from random import randrange
from random import randint
from loggingChannel import sendLog
import os, os.path
import requests
import json
from dotenv import load_dotenv
from fileManager import sendImage, sendImageNew
from minecraftrcon import ping_MC_server, ping_MC_server_ctx
import russianroulette


async def sendGif(client, channel, search_term, random):
    # gif start
    load_dotenv()
    apikey = os.getenv('TENOR_API_KEY')
    lmt = 50
    url = "https://api.tenor.com/v1/search?q="
    if random:
        url = "https://api.tenor.com/v1/random?q="
        lmt = 1
    r = requests.get(url + ("%s&key=%s&limit=%s" % (search_term, apikey, lmt)))
    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_gifs = json.loads(r.content)
        # print(top_gifs)
        selected_gif = top_gifs['results'][randrange(lmt)]
        print(await sendLog(log=("Gif selected " + selected_gif["url"]), client=client))
        await channel.send(selected_gif["url"])
    else:
        top_8gifs = None

async def sendGifNew(ctx, client, search_term, random):
    # gif start
    load_dotenv()
    apikey = os.getenv('TENOR_API_KEY')
    lmt = 50
    url = "https://api.tenor.com/v1/search?q="
    if random:
        url = "https://api.tenor.com/v1/random?q="
        lmt = 1
    r = requests.get(url + ("%s&key=%s&limit=%s" % (search_term, apikey, lmt)))
    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_gifs = json.loads(r.content)
        # print(top_gifs)
        selected_gif = top_gifs['results'][randrange(lmt)]
        print(await sendLog(log=("Gif selected " + selected_gif["url"]), client=client))
        await ctx.send(selected_gif["url"])
    else:
        top_8gifs = None


async def getGif(client, search_term, random):
    # gif start
    load_dotenv()
    apikey = os.getenv('TENOR_API_KEY')
    lmt = 50
    url = "https://api.tenor.com/v1/search?q="
    if random:
        url = "https://api.tenor.com/v1/random?q="
        lmt = 1
    r = requests.get(url + ("%s&key=%s&limit=%s" % (search_term, apikey, lmt)))
    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_gifs = json.loads(r.content)
        # print(top_gifs)
        selected_gif = top_gifs['results'][randrange(lmt)]
        print(await sendLog(log=("Gif selected " + selected_gif["url"]), client=client))
        return selected_gif["url"]
    else:
        top_8gifs = None
    return "https://media2.giphy.com/media/YyKPbc5OOTSQE/giphy.gif"


async def anime(ctx, client):
    localOrOnline = randint(1, 3)
    if localOrOnline >= 2:  # Online
        # print(await sendLog(
            # log=f'{message.author.name} has requested anime! Sending online gif!',
            # client=client))
        await sendGifNew(ctx, client, "cute anime girl", random=False)
    else:
        DIR = './images/anime/'
        options = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        animeNum = random.randint(0, (options - 1))
        # print(await sendLog(
            # log=f'{message.author.name} has requested anime! Sending anime#{animeNum}!',
            # client=client))
        await sendImageNew(ctx, client, "anime_", animeNum, DIR)


async def selfie(ctx, client):
    DIR = './images/selfies/'
    options = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    selfieNum = random.randint(0, (options - 1))
    print(await sendLog(
        log=f'{ctx.author.name} has asked for a selfie. Sending -> #{selfieNum}!',
        client=client))
    await sendImageNew(ctx, client, "selfie_", selfieNum, DIR)


async def punch(ctx, client, mentions):
    if mentions.id == 786698404927504385:
        embed = discord.Embed(title=f"Punching {ctx.author.name}", colour=discord.Colour(0xff0000),
                              description=f"Rest in peace {ctx.author.mention}. You better not try to hurt her again...")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name="Steve from Accounting",
                         icon_url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot/blob/master/images/punch_icon.png?raw=true")
        searchTerm = "anime punch"
    else:
        embed = discord.Embed(title=f"Punching {mentions.name}", colour=discord.Colour(0xff0000),
                              description=f"Rest in peace {mentions.mention}")
        embed.set_thumbnail(url=mentions.avatar_url)
        rng = randint(1, 2)
        if rng == 2:
            searchTerm = "punch"
        else:
            searchTerm = "anime punch"
        embed.set_author(name="Steve from Accounting",
                         icon_url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot/blob/master/images/punch_icon.png?raw=true")
    await ctx.send(embed=embed)
    await sendGifNew(ctx, client, searchTerm, random=False)


async def mcinfo(ctx, client):
    await ping_MC_server_ctx(client, ctx)


async def tpdne(ctx):
    url = "https://fakeface.rest/face/json"
    r = requests.get(url)
    if r.status_code == 200:
        thispersondoesnotexist = json.loads(r.content)
        await ctx.send(thispersondoesnotexist['image_url'])


async def waifu(ctx):
    url = "https://www.thiswaifudoesnotexist.net/example-"
    num = random.randint(0, 100000)
    await ctx.send(url + str(num) + ".jpg")


async def joke(ctx):
    num = random.randint(0, 3)
    if num >= 1:
        print("Sending joke from joke3.p.rapidapi")
        url = "https://joke3.p.rapidapi.com/v1/joke"
        headers = {
            'x-rapidapi-key': "dc02b90e2emsh6be8145fc6dd65ep198267jsnf83b7e473ef7",
            'x-rapidapi-host': "joke3.p.rapidapi.com"
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            joke = json.loads(r.content)
            await ctx.send(joke['content'])
        else:
            await ctx.send("Failed to load joke. Please try again later.")
    else:
        print("Sending joke from sv443.net/jokeapi")
        url = "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=racist&type=single"
        r = requests.get(url)
        if r.status_code == 200:
            joke = json.loads(r.content)
            await ctx.send(joke['joke'])
        await ctx.send("Failed to load joke. Please try again later.")

async def checkForCommands(message, client, member_database):
    if search("^(anime)", message.content.lower()):
        localOrOnline = randint(1, 3)
        if localOrOnline >= 2:  # Online
            print(await sendLog(
                log=f'{message.author.name} has requested anime! Sending online gif!',
                client=client))
            await sendGif(client, message.channel, "cute anime girl", random=False)
        else:
            DIR = './images/anime/'
            options = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            animeNum = random.randint(0, (options - 1))
            print(await sendLog(
                log=f'{message.author.name} has requested anime! Sending anime#{animeNum}!',
                client=client))
            await sendImage(message, client, "anime_", animeNum, DIR)

    if search("^(selfie)", message.content.lower()):
        DIR = './images/selfies/'
        options = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        selfieNum = random.randint(0, (options - 1))
        print(await sendLog(
            log=f'{message.author.name} has asked for a selfie. Sending -> #{selfieNum}!',
            client=client))
        await sendImage(message, client, "selfie_", selfieNum, DIR)

    if search("^(rr|russian roulette|russianroulette|roulette)", message.content.lower()):
        await russianroulette.startGame(message, client)

    if search("^(shoot|rrshoot|rr shoot)", message.content.lower()):
        await russianroulette.shoot(message, client)

    if search("^(spin|rrspin|rr spin)", message.content.lower()):
        await russianroulette.spin(message, client)

    if search("roll(_|\s)([0-9]+)d([0-9]+)", message.content.lower()):
        value = 0
        dice = [int(i) for i in message.content.split() if i.isdigit()]

        print(len(dice))
        if len(dice) == 2:
            for i in range(dice[0]):
                value = value + dice[1]
            embed = discord.Embed(colour=discord.Colour(0x259944), url="https://discordapp.com",
                                  description=f'You rolled {value} on your {dice[0]}d{dice[1]}. Good job! At the very least you get an A+ for effort so isn\'t that nice.')
            embed.set_thumbnail(url="https://gilkalai.files.wordpress.com/2017/09/dice.png?w=640")
            embed.set_author(name="Steve from Accounting", url="https://www.google.com/error",
                             icon_url="https://www.topaccountingdegrees.org/wp-content/uploads/2015/08/Accounting-7.jpg")
            await message.channel.send(embed=embed)

    # Sins
    if search("^(sins)", message.content.lower()):
        async with message.channel.typing():
            mentions = message.mentions
            sins_found = False
            if len(mentions) > 0:
                for member in member_database:
                    if member['userID'] == mentions[0].id:
                        sins_found = True
                        member_sins = member
                if sins_found:
                    embed = discord.Embed(title=f"Sins of {mentions[0].display_name}", colour=discord.Colour(0x781dac),
                                          description=member_sins['sins'])
                    embed.set_thumbnail(url=mentions[0].avatar_url)
                    embed.set_author(name="The Devil", url="https://youtu.be/dQw4w9WgXcQ",
                                     icon_url="https://i.imgur.com/uLAimaY_d.webp?maxwidth=728&fidelity=grand")
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send('You need to @ mention someone to see their sins.')

    # Punch
    if search("^(punch)", message.content.lower()):
        mentions = message.mentions
        if len(mentions) > 0:
            async with message.channel.typing():
                if mentions[0].id == 786698404927504385:
                    embed = discord.Embed(title=f"Punching {message.author.name}", colour=discord.Colour(0xff0000),
                                          description=f"Rest in peace {message.author.mention}. You better not try to hurt her again...")
                    embed.set_thumbnail(url=message.author.avatar_url)
                    embed.set_author(name="Steve from Accounting",
                                     icon_url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot/blob/master/images/punch_icon.png?raw=true")
                    searchTerm = "anime punch"
                else:
                    embed = discord.Embed(title=f"Punching {mentions[0].name}", colour=discord.Colour(0xff0000),
                                          description=f"Rest in peace {mentions[0].mention}")
                    embed.set_thumbnail(url=mentions[0].avatar_url)
                    rng = randint(1, 2)
                    if rng == 2:
                        searchTerm = "punch"
                    else:
                        searchTerm = "anime punch"
                    embed.set_author(name="Steve from Accounting",
                                     icon_url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot/blob/master/images/punch_icon.png?raw=true")
                await message.channel.send(embed=embed)
                await sendGif(client, message.channel, searchTerm, random=False)
        else:
            await message.channel.send('You need to @ mention your enemy to punch them.')

    # Grank
    # if search("^(grank)", message.content.lower()):
    # await message.channel.send('[THIS WILL SHOW RANK BUT IT\'S UNDER CONSTRUCTION]')

    if search("^(mcinfo)", message.content.lower()):
        async with message.channel.typing():
            await ping_MC_server(client, message)

    if search("^(ping)", message.content.lower()):
        await message.channel.send('What are you expecting? Me to say pong back?')

    if search("^(wtf)", message.content.lower()):
        await message.channel.send('Rude!')

    if search("^(nani)", message.content.lower()):
        await message.channel.send('何')

    if search("^(thispersondoesnotexist|tpdne)", message.content.lower()):
        async with message.channel.typing():
            url = "https://fakeface.rest/face/json"
            r = requests.get(url)
            if r.status_code == 200:
                thispersondoesnotexist = json.loads(r.content)
                await message.channel.send(thispersondoesnotexist['image_url'])

    if search("^(waifu)", message.content.lower()):
        async with message.channel.typing():
            url = "https://www.thiswaifudoesnotexist.net/example-"
            num = random.randint(0, 100000)
            await message.channel.send(url + str(num) + ".jpg")

    if search("^((id)|(fake(\s|_|)id))", message.content.lower()):
        async with message.channel.typing():
            url = "https://random-user.p.rapidapi.com/getuser"

            headers = {
                'x-rapidapi-key': os.getenv('X_RAPIDAPI_KEY'),
                'x-rapidapi-host': "random-user.p.rapidapi.com"
            }

            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                id = json.loads(r.content)
                id = id['results'][0]
                print(id)
                embed = discord.Embed(colour=discord.Colour(0xb8b8b8),
                                      description=f'ID for {id["name"]["first"]} {id["name"]["last"]}:')

                embed.set_thumbnail(url=id["picture"]["large"])
                embed.set_author(name=f'{id["name"]["title"]} {id["name"]["first"]} {id["name"]["last"]}',
                                 icon_url=id["picture"]["large"], url=id["picture"]["large"])
                location = id["location"]
                embed.add_field(name="Location",
                                value=f'{location["street"]["number"]} {location["street"]["name"]} {location["city"]}, {location["state"]}, {location["country"]}, {location["postcode"]}')
                embed.add_field(name="Email",
                                value=f'Email: {id["email"]} \nUsername: {id["login"]["username"]} \nPassword: {id["login"]["password"]}')
                embed.add_field(name="Phone Number", value=f'{id["cell"]}')
                embed.add_field(name="Date of Birth", value=f'Age: {id["dob"]["age"]} DOB: {id["dob"]["date"]}')
                if id['id']['value'] == id['id']['value'] and id['id']['value'] is not None:
                    embed.add_field(name="ID", value=f'Type: {id["id"]["name"]} Value: {id["id"]["value"]}')

                await message.channel.send(embed=embed)

    if search("^(hot)", message.content.lower()):
        file = discord.File("./video/Hot.mp4", filename="hot.mp4")
        await message.channel.send(file=file)

    if search("^(joke)", message.content.lower()):
        async with message.channel.typing():
            num = random.randint(0, 3)
            if num >= 1:
                print("Sending joke from joke3.p.rapidapi")
                url = "https://joke3.p.rapidapi.com/v1/joke"
                headers = {
                    'x-rapidapi-key': "dc02b90e2emsh6be8145fc6dd65ep198267jsnf83b7e473ef7",
                    'x-rapidapi-host': "joke3.p.rapidapi.com"
                }
                r = requests.get(url, headers=headers)
                if r.status_code == 200:
                    joke = json.loads(r.content)
                    await message.channel.send(joke['content'])
            else:
                print("Sending joke from sv443.net/jokeapi")
                url = "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=racist&type=single"
                r = requests.get(url)
                if r.status_code == 200:
                    joke = json.loads(r.content)
                    await message.channel.send(joke['joke'])

    if search("^(insult)", message.content.lower()):
        async with message.channel.typing():
            url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
            r = requests.get(url)
            if r.status_code == 200:
                insult = json.loads(r.content)
                await message.channel.send(insult['insult'])

    if search("^(fact)", message.content.lower()):
        async with message.channel.typing():
            url = "https://uselessfacts.jsph.pl/random.json?language=en"
            r = requests.get(url)
            if r.status_code == 200:
                fact = json.loads(r.content)
                await message.channel.send(fact['text'])

    if search("^(advi(s|c)e)", message.content.lower()):
        async with message.channel.typing():
            url = "https://api.adviceslip.com/advice"
            r = requests.get(url)
            if r.status_code == 200:
                advice = json.loads(r.content)
                await message.channel.send(advice["slip"]['advice'])

    if search("^(cat|kitty)", message.content.lower()):
        async with message.channel.typing():
            cat_api = os.getenv('THE_CAT_API')
            url = "https://api.thecatapi.com/v1/images/search?api_key=" + cat_api
            r = requests.get(url)
            if r.status_code == 200:
                cat = json.loads(r.content)
                await message.channel.send(cat[0]["url"])

    if search("^(dog|pup)", message.content.lower()):
        async with message.channel.typing():
            url = "https://random.dog/woof.json?ref=apilist.fun"
            r = requests.get(url)
            if r.status_code == 200:
                dog = json.loads(r.content)
                await message.channel.send(dog["url"])

    if search("^(yesorno)", message.content.lower()):
        async with message.channel.typing():
            url = "https://yesno.wtf/api"
            r = requests.get(url)
            if r.status_code == 200:
                yesorno = json.loads(r.content)
                await message.channel.send(yesorno['image'])
                await message.channel.send(yesorno['answer'].capitalize())

    if search("^(zerotier)", message.content.lower()):
        await message.channel.send('[THIS WILL SHOW YOU HOW TO SETUP ZERO TIER BUT IT\'S UNDER CONSTRUCTION]')

    if search("^(r2loadout)", message.content.lower()):
        async with message.channel.typing():
            from r2loadout import get_r2loadout
            await message.channel.send(embed=get_r2loadout())

    if search("^(random)", message.content.lower()):
        await message.channel.send('[THIS WILL SEND A RANDOM COMMAND BUT IT\'S UNDER CONSTRUCTION]')

    if search("^(help)", message.content.lower()):
        async with message.channel.typing():
            embed = discord.Embed(title="Help", colour=discord.Colour(0x9b9b9b), url="https://discordapp.com",
                                  description="This is a list of commands you can use with Geoffery's Son."
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
                                              "\n\n**!anime**\nAnime gifs for everyone!"
                                              "\n\n**!roll 1d6**\nRolls dice based on what you send. For example !roll 3d2 will roll 3 d2 dice and than send the result."
                                              "\n\n**!sins @yourfiends**\nThis where inform you of the sins of your friends. I'd watch out for Steve from accounting..."
                                              "\n\n**!punch @yourfiends**\nPunch your friends over the internet from a safe distance."
                                              "\n\n**!mcinfo**\nInfo on the Minecraft Server if one is running."
                                              "\n\n**!ping**\nWhat do you expect?"
                                              "\n\n**!wtf**\nWhy is this a command?"
                                              "\n\n**!nani**\nIt can translate to weeb characters."
                                              "\n\n**!thispersondoesnotexist or !tpdne**\nThe smart ai over at [thispersondoesnotexist](https://thispersondoesnotexist.com) will send us a face that does not exist."
                                              "\n\n**!waifu**\nThe smart ai over at [thiswaifudoesnotexist](https://www.thiswaifudoesnotexist.net) will send us a waifu that does not exist."
                                              "\n\n**!id or !fake id**\nThis will create your new identity."
                                              "\n\n**!hot**\nBRRRRRRRR!!"
                                              "\n\n**!joke**\nI'll tell you a joke!"
                                              "\n\n**!insult**\nI'll insult you! Be prepared some of these are pretty terrible..."
                                              "\n\n**!fact**\nI'll tell you a random fact."
                                              "\n\n**!advice**\nI'll give you some advice."
                                              "\n\n**!cat or !dog**\nI'll send a random image of a kitty or dogo!"
                                              "\n\n**!yesorno**\nI'll tell you if the answer is yes or no."
                                              "\n\n**!r2loadout**\nA random load out for a Risk of Rain 2 Command run. I hope Rnjesus is on your side."
                                              "\n\n**!rr**\nStart a game of Russian Roulette."
                                              "\n\n**!help**\nConsidering your already here you probably already know this one...")

            embed.set_author(name="Geoffery's Son", url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot",
                             icon_url="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot/blob/Python/images/selfies/selfie_04.png?raw=true")
            try:
                await message.delete()
            except Exception:
                print("Failed to delete message...")
            await message.author.send(embed=embed)
