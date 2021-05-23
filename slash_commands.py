from time import sleep

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


async def sins(ctx, client, mention, member_database):
    sins_found = False
    for member in member_database:
        if member['userID'] == mention.id:
            sins_found = True
            member_sins = member
    if sins_found:
        embed = discord.Embed(title=f"Sins of {mention.display_name}", colour=discord.Colour(0x781dac),
                              description=member_sins['sins'])
        embed.set_thumbnail(url=mention.avatar_url)
        embed.set_author(name="The Devil", url="https://youtu.be/dQw4w9WgXcQ",
                         icon_url="https://i.imgur.com/uLAimaY_d.webp?maxwidth=728&fidelity=grand")
        await ctx.send(embed=embed)


async def fake_id(ctx):
    url = "https://random-user.p.rapidapi.com/getuser"

    headers = {
        'x-rapidapi-key': os.getenv('X_RAPIDAPI_KEY'),
        'x-rapidapi-host': "random-user.p.rapidapi.com"
    }

    print("Getting request")
    r = requests.get(url, headers=headers)
    print(f"Request Code: {r.status_code}")
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

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Command failed due to server error {r.status_code}. Please try again later. <:cry_anime:557425672260288512>")


async def joke(ctx):
    num = random.randint(0, 3)
    num = 1
    if num >= 1:
        print("Sending joke from joke3.p.rapidapi")
        url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"
        querystring = {"type": "single,twopart", "format": "json", "idRange": "0-150",
                       "blacklistFlags": "nsfw,racist"}
        headers = {
            'x-rapidapi-key': "3760b526d1msh34c2122de2b24dcp1f5f20jsn6a233a68122f",
            'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com"
        }
        r = requests.request("GET", url, headers=headers, params=querystring)
        if r.status_code == 200:
            joke = json.loads(r.content)
            if joke['type'] == 'twopart':
                await ctx.send(joke['setup'])
                sleep(5)
                await ctx.send(joke['delivery'])
            else:
                await ctx.send(joke['joke'])
        else:
            await ctx.send(
                f"Command failed due to server error {r.status_code}. Please try again later. <:cry_anime:557425672260288512>")
    else:
        print("Sending joke from sv443.net/jokeapi")
        url = "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=racist&type=single"
        r = requests.get(url)
        if r.status_code == 200:
            joke = json.loads(r.content)
            await ctx.channel.send(joke['joke'])
        else:
            await ctx.send(
                f"Command failed due to server error {r.status_code}. Please try again later. <:cry_anime:557425672260288512>")
