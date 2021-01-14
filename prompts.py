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

    if search("(^|\s)(sand)($|\s|!)", message.content.lower()):
        await message.channel.send("https://pa1.narvii.com/6995/64746a9cf49d6c306c861b2c0d0029b6be40c807r1-480-240_hq.gif")

    if search("(the sun is a deadly la(z|s)er)", message.content.lower()):
        file = discord.File("./video/Blanket.mp4", filename="video.mp4")
        await message.channel.send(file=file)

    if search("^10th time", message.content.lower()):
        await message.channel.send("9th time!")

    if search("^9th time", message.content.lower()):
        await message.channel.send("10th time!")

    if search("(^|\s)(badonkers|dobonhonkeros|dohoonkabhankoloos|tonhongerekoogers|serious honkers|bonkhonagahoogs|humungous hungolomghnonoloughongous|new anime plot)($|\s|!)", message.content.lower()):
        await message.channel.send("https://www.youtube.com/watch?v=7yaCKsb0vUg")

    if search("(^|\s)(sauce)($|\s|!)", message.content.lower()):
        sauceNum = random.randint(0,321861)

        print(await sendLog(log=f'{message.author.name} requested sauce. The sauce found was: {sauceNum} \nhttps://nhentai.net/g/{sauceNum}', client=client))
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

    if search("(^|\s)(ravioli ravioli)($|\s|!)", message.content.lower()):
        file = discord.File("./images/ravioli.gif", filename="ravioli.gif")
        await message.channel.send(file=file)

    if search("(^|\s)(hentai)($|\s|!)", message.content.lower()):
        file = discord.File("./images/hentai.gif", filename="hentai.gif")
        await message.channel.send(file=file)

    if search("(^|\s)(hello there)($|\s|!)", message.content.lower()):
        file = discord.File("./images/generalkenobi.gif", filename="generalkenobi.gif")
        await message.channel.send(file=file)

    if search("(^|\s)(trap)(s|$|\s|!)(s|$|\s|!)", message.content.lower()):
        file = discord.File("./images/trap.gif", filename="trap.gif")
        await message.channel.send(file=file)

    if search("(g|.|\s|j|^)wentworth($|\s|!)", message.content.lower()):
        await message.channel.send("877-CASH-NOW!")

    if search("\sa scratch($|\s|!)", message.content.lower()):
        await message.channel.send("http://www.okmoviequotes.com/wp-content/uploads/2014/05/402-Monty-Python-and-the-Holy-Grail-quotes.gif")
