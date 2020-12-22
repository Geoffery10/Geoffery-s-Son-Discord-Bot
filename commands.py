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



