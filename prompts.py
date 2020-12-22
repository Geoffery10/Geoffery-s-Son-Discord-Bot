import discord
from re import search
import random
from loggingChannel import sendLog
import os, os.path
from fileManager import sendImage


async def checkForPrompts(message, client):
    # owo
    if search("(^|\s)(u|o|♡|Ò|□|●|0)(u|w)(u|o|♡|Ó|□|●|0)", message.content.lower()):
        file = discord.File("./images/owo.png", filename="image.png")
        await message.channel.send(file=file)

    if search("(is it possible to learn this power)", message.content.lower()):
        file = discord.File("./video/Palpatine_00.mp4", filename="palpatine.mp4")
        await message.channel.send(file=file)

    if search("(the sun is a deadly la(z|s)er)", message.content.lower()):
        file = discord.File("./video/Blanket.mp4", filename="video.mp4")
        await message.channel.send(file=file)

    if search("^10th time", message.content.lower()):
        await message.channel.send("9th time!")

    if search("^9th time", message.content.lower()):
        await message.channel.send("10th time!")

    if search("(^|\s)(sauce)($|\s)", message.content.lower()):
        sauceNum = random.randint(0,321861)

        print(await sendLog(log=f'{message.author.name} requested sauce. The sauce found was: {sauceNum} \nhttps://nhentai.com/g/{sauceNum}', client=client))
        description = "Here is the sauce in which you desire: " + str(sauceNum)
        embed = discord.Embed(colour=discord.Colour(0xed2553), url="https://discordapp.com",
                              description=description)
        embed.set_author(name="The Devil", url="https://youtu.be/dQw4w9WgXcQ",
                         icon_url="https://i.imgur.com/uLAimaY_d.webp?maxwidth=728&fidelity=grand")
        await message.channel.send(embed=embed)

    if search("(^|\s)(heresy)($|\s)", message.content.lower()):
        DIR = './images/heresy/'
        options = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        heresyNum = random.randint(0, (options-1))
        print(await sendLog(
            log=f'{message.author.name} has detected heresy! Sending heresy#{heresyNum}!',
            client=client))
        await sendImage(message, client, "heresy_", heresyNum, DIR)

    if search("ravioli ravioli", message.content.lower()):
        file = discord.File("./images/ravioli.gif", filename="ravioli.gif")
        await message.channel.send(file=file)
