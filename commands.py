import discord
from re import search
import random
from random import randrange
from loggingChannel import sendLog
import os, os.path
import requests
import json
from dotenv import load_dotenv
from fileManager import sendImage


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


async def checkForCommands(message, client):
    if search("^(anime)", message.content.lower()):
        await sendGif(client, message.channel, "cute anime girl", random=False)

    if search("^(selfie)", message.content.lower()):
        DIR = './images/selfies/'
        options = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        selfieNum = random.randint(0, (options - 1))
        print(await sendLog(
            log=f'{message.author.name} has asked for a selfie. Sending -> #{selfieNum}!',
            client=client))
        await sendImage(message, client, "selfie_", selfieNum, DIR)

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
        await message.channel.send('[THIS WILL SHOW YOU PEOPLES SINS BUT IT\'S UNDER CONSTRUCTION]')

    # Punch
    if search("^(punch)", message.content.lower()):
        await message.channel.send('[THIS WILL PUNCH PEOPLE BUT IT\'S UNDER CONSTRUCTION]')

    # Grank
    # if search("^(grank)", message.content.lower()):
    # await message.channel.send('[THIS WILL SHOW RANK BUT IT\'S UNDER CONSTRUCTION]')

    if search("^(mcinfo)", message.content.lower()):
        url = "https://api.ipify.org/?format=json"
        ip = "error"
        r = requests.get(url)
        if r.status_code == 200:
            ip = json.loads(r.content)
            print(f'IP: {ip["ip"]}')
        await message.channel.send(f'Minecraft Server IP: {ip["ip"]}:26969')

    if search("^(ping)", message.content.lower()):
        await message.channel.send('What are you expecting? Me to say pong back?')

    if search("^(wtf)", message.content.lower()):
        await message.channel.send('Rude!')

    if search("^(nani)", message.content.lower()):
        await message.channel.send('何')

    if search("^(thispersondoesnotexist|tpdne)", message.content.lower()):
        url = "https://fakeface.rest/face/json"
        r = requests.get(url)
        if r.status_code == 200:
            thispersondoesnotexist = json.loads(r.content)
            # print(top_gifs)
            await message.channel.send(thispersondoesnotexist['image_url'])

    if search("^(waifu)", message.content.lower()):
        url = "https://www.thiswaifudoesnotexist.net/example-"
        num = random.randint(0, 100000)
        await message.channel.send(url + str(num) + ".jpg")

    if search("^((id)|(fake(\s|_|)id))", message.content.lower()):
        url = "https://random-user.p.rapidapi.com/getuser"

        headers = {
            'x-rapidapi-key': "dc02b90e2emsh6be8145fc6dd65ep198267jsnf83b7e473ef7",
            'x-rapidapi-host': "random-user.p.rapidapi.com"
        }

        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            id = json.loads(r.content)
            id = id['results'][0]
            print(id)
            embed = discord.Embed(colour=discord.Colour(0xb8b8b8), description=f'ID for {id["name"]["first"]} {id["name"]["last"]}:')

            embed.set_thumbnail(url=id["picture"]["large"])
            embed.set_author(name=f'{id["name"]["title"]} {id["name"]["first"]} {id["name"]["last"]}',
                             icon_url=id["picture"]["large"], url=id["picture"]["large"])
            location = id["location"]
            embed.add_field(name="Location", value=f'{location["street"]["number"]} {location["street"]["name"]} {location["city"]}, {location["state"]}, {location["country"]}, {location["postcode"]}')
            embed.add_field(name="Email", value=f'Email: {id["email"]} \nUsername: {id["login"]["username"]} \nPassword: {id["login"]["password"]}')
            embed.add_field(name="Phone Number", value=f'{id["cell"]}')
            embed.add_field(name="Date of Birth", value=f'Age: {id["dob"]["age"]} DOB: {id["dob"]["date"]}')
            if id['id']['value'] == id['id']['value'] and id['id']['value'] is not None:
                embed.add_field(name="ID", value=f'Type: {id["id"]["name"]} Value: {id["id"]["value"]}')

            await message.channel.send(embed=embed)

    if search("^(hot)", message.content.lower()):
        file = discord.File("./video/Hot.mp4", filename="hot.mp4")
        await message.channel.send(file=file)

    if search("^(joke)", message.content.lower()):
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
        url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        r = requests.get(url)
        if r.status_code == 200:
            insult = json.loads(r.content)
            await message.channel.send(insult['insult'])

    if search("^(fact)", message.content.lower()):
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        r = requests.get(url)
        if r.status_code == 200:
            fact = json.loads(r.content)
            await message.channel.send(fact['text'])

    if search("^(advi(s|c)e)", message.content.lower()):
        url = "https://api.adviceslip.com/advice"
        r = requests.get(url)
        if r.status_code == 200:
            advice = json.loads(r.content)
            await message.channel.send(advice["slip"]['advice'])

    if search("^(cat|kitty)", message.content.lower()):
        cat_api = os.getenv('THE_CAT_API')
        url = "https://api.thecatapi.com/v1/images/search?api_key=" + cat_api
        r = requests.get(url)
        if r.status_code == 200:
            cat = json.loads(r.content)
            await message.channel.send(cat[0]["url"])

    if search("^(dog|pup)", message.content.lower()):
        url = "https://random.dog/woof.json?ref=apilist.fun"
        r = requests.get(url)
        if r.status_code == 200:
            dog = json.loads(r.content)
            await message.channel.send(dog["url"])

    if search("^(yesorno)", message.content.lower()):
        url = "https://yesno.wtf/api"
        r = requests.get(url)
        if r.status_code == 200:
            yesorno = json.loads(r.content)
            await message.channel.send(yesorno['image'])

    if search("^(zerotier)", message.content.lower()):
        await message.channel.send('[THIS WILL SHOW YOU HOW TO SETUP ZERO TIER BUT IT\'S UNDER CONSTRUCTION]')

    if search("^(r2loadout)", message.content.lower()):
        await message.channel.send('[THIS WILL CREATE A RANDOM LOADOUT FOR YOU BUT IT\'S UNDER CONSTRUCTION]')

    if search("^(random)", message.content.lower()):
        await message.channel.send('[THIS WILL SEND A RANDOM COMMAND BUT IT\'S UNDER CONSTRUCTION]')

    if search("^(help)", message.content.lower()):
        await message.channel.send('[LOOKS LIKE YOU NEED HELP... TOO BAD IT\'S UNDER CONSTRUCTION. ASK GEOFFERY.]')
