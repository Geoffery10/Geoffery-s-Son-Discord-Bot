import discord
from re import search
import random
from loggingChannel import sendLog
import os.path
from os import path
from discord.ext import commands


async def sendImage(message, client, fileName, num, dir):
    found = True
    if num <= 9:
        fileName = fileName + "0" + str(num)
    else:
        fileName = fileName + str(num)

    if path.isfile(dir + fileName + ".gif"):
        print(f'Found {(dir + fileName + ".gif")}')
        file = discord.File(dir + fileName + ".gif", filename="image.gif")
    elif path.isfile(dir + fileName + ".png"):
        print(f'Found {(dir + fileName + ".png")}')
        file = discord.File(dir + fileName + ".png", filename="image.png")
    elif path.isfile(dir + fileName + ".jpg"):
        print(f'Found {(dir + fileName + ".jpg")}')
        file = discord.File(dir + fileName + ".jpg", filename="image.jpg")
    elif path.isfile(dir + fileName + ".mp4"):
        print(f'Found {(dir + fileName + ".mp4")}')
        file = discord.File(dir + fileName + ".mp4", filename="video.mp4")
    elif path.isfile(dir + fileName + ".mov"):
        print(f'Found {(dir + fileName + ".mov")}')
        file = discord.File(dir + fileName + ".mov", filename="video.mov")
    else:
        print(await sendLog(log=f'This ain\'t it chief. I couldn\'t find the gif.', client=client))
        found = False

    if found:
        await message.channel.send(file=file)


async def sendImageNew(interaction, client, fileName, num, dir):
    found = True
    if num <= 9:
        fileName = fileName + "0" + str(num)
    else:
        fileName = fileName + str(num)

    if path.isfile(dir + fileName + ".gif"):
        print(f'Found {(dir + fileName + ".gif")}')
        file = discord.File(dir + fileName + ".gif", filename="image.gif")
    elif path.isfile(dir + fileName + ".png"):
        print(f'Found {(dir + fileName + ".png")}')
        file = discord.File(dir + fileName + ".png", filename="image.png")
    elif path.isfile(dir + fileName + ".jpg"):
        print(f'Found {(dir + fileName + ".jpg")}')
        file = discord.File(dir + fileName + ".jpg", filename="image.jpg")
    elif path.isfile(dir + fileName + ".mp4"):
        print(f'Found {(dir + fileName + ".mp4")}')
        file = discord.File(dir + fileName + ".mp4", filename="video.mp4")
    elif path.isfile(dir + fileName + ".mov"):
        print(f'Found {(dir + fileName + ".mov")}')
        file = discord.File(dir + fileName + ".mov", filename="video.mov")
    else:
        print(await sendLog(log=f'This ain\'t it chief. I couldn\'t find the gif.', client=client))
        found = False

    if found:
        await interaction.response.send_message(file=file)
