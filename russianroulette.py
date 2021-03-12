import discord
from loggingChannel import sendLog
import requests
import json
import os
import os.path
from os import path
from random import randint
from dotenv import load_dotenv

example_roulette_data = {
    "guild": 786690956514426910,
    "channel": 786690957042516001,
    "active": False,
    "players": [253710834553847808],
    "bullet_index": 6,
    "current_index": 1
}

default_thumbnail = "https://ctl.s6img.com/society6/img/Dabrw_Qve91Mq4FyNPHsbqz-84k/w_700/prints/~artwork/s6-0013/a" \
                    "/4390483_6932973/~~/russian-roulette-rts-prints.jpg "


async def fixNick(member):
    if member.nick == None or member.nick == "None":
        return member.name
    return member.nick


async def check_game_file():
    return path.exists('./gameData/Russian Roulette/games.json')


async def get_game_data():
    with open("./gameData/Russian Roulette/games.json", "r") as read_file:
        game_data_set = json.load(read_file)
    return game_data_set


async def save_game_data(game_data_set, message):
    new_game = {
        "guild": message.guild.id,
        "channel": message.channel.id,
        "active": True,
        "players": [message.author.id],
        "bullet_index": randint(1, 6),
        "current_index": 1
    }
    game_data_set.append(new_game)
    print("Creating new game data")
    with open("./gameData/Russian Roulette/games.json", "w") as write_file:
        json.dump(game_data_set, write_file, indent=4)


async def update_game_data(game_data_set, new_data):
    print("Updating game data")
    index = 0
    for index in range(len(game_data_set)):
        if game_data_set[index]["channel"] == new_data["channel"]:
            game_data_set[index] = new_data
            print("Found Data to Update")
    with open("./gameData/Russian Roulette/games.json", "w") as write_file:
        json.dump(game_data_set, write_file, indent=4)


async def check_for_game(message, game_data_set):
    data = {}
    game_found = False
    for data_set in game_data_set:
        if str(data_set["channel"]) == str(message.channel.id):
            print("Game found on this channel")
            game_found = True
            data = data_set
            break
    return game_found, data


async def game_message(message, description, thumbnail):
    embed = discord.Embed(title="Russian Roulette", colour=discord.Colour(0x69645f), url="http://government.ru/en/",
                          description=description)
    embed.set_thumbnail(
        url=thumbnail)
    embed.set_author(name="Vladimir Putin", url="http://government.ru/en/",
                     icon_url="https://media.vanityfair.com/photos/5874192bee23284912086649/1:1/w_960,h_960,"
                              "c_limit/vladimir-putin-evil.jpg")
    await message.channel.send(embed=embed)


async def shoot(message, client):
    nick = await fixNick(message.author)
    if await check_game_file():
        game_found = False
        print("GAME DATA FOUND")
        game_data_set = await get_game_data()
        game_found, data = await check_for_game(message, game_data_set)
        if game_found:
            if data["active"]:
                if data["current_index"] == data["bullet_index"]:
                    data["active"] = False
                    await game_message(message, f"<:rip:372950049665318925> {nick} you will be missed...",
                                       message.author.avatar_url)
                else:
                    data["current_index"] += 1
                    if data["current_index"] > 6:
                        data["current_index"] = 1
                    await game_message(message, f"Seems you get to live today {nick}...", message.author.avatar_url)
                if message.author.id not in data["players"]:
                    data["players"].append(message.author.id)
                await update_game_data(game_data_set, data)
            else:
                await startGame(message, client)
        else:
            await startGame(message, client)
    else:
        await game_message(message, "Game failed to start... Please try again later.", default_thumbnail)


async def spin(message, client):
    nick = await fixNick(message.author)
    if await check_game_file():
        game_found = False
        print("GAME DATA FOUND")
        game_data_set = await get_game_data()
        game_found, data = await check_for_game(message, game_data_set)
        if game_found:
            if data["active"]:
                data["current_index"] = randint(1, 6)
                if data["current_index"] == data["bullet_index"]:
                    data["active"] = False
                    await game_message(message,
                                       f"<:rip:372950049665318925> {nick} you will be missed...",
                                       message.author.avatar_url)
                else:
                    data["current_index"] += 1
                    if data["current_index"] > 6:
                        data["current_index"] = 0
                    await game_message(message, f"Seems you get to live today {nick}...",
                                       message.author.avatar_url)
                if message.author.id not in data["players"]:
                    data["players"].append(message.author.author.id)
                await update_game_data(game_data_set, data)
            else:
                await startGame(message, client)
        else:
            await startGame(message, client)
    else:
        await game_message(message, "Game failed to start... Please try again later.", default_thumbnail)


async def startGame(message, client):
    if await check_game_file():
        game_found = False
        print("GAME DATA FOUND")
        game_data_set = await get_game_data()
        game_found, data = await check_for_game(message, game_data_set)
        if game_found:
            await game_message(message, "Starting Game... Use !shoot to shoot and !spin to spin. (Note spin "
                                        "will also shoot you with whatever it lands on..)", default_thumbnail)
            new_data = {
                "guild": message.guild.id,
                "channel": message.channel.id,
                "active": True,
                "players": [message.author.id],
                "bullet_index": randint(1, 6),
                "current_index": 1
            }
            await update_game_data(game_data_set, new_data)
        else:
            print("No game was found for this channel")
            await save_game_data(game_data_set, message)
            await game_message(message, "Starting Game... Use !shoot to shoot and !spin to spin. (Note spin "
                                        "will also shoot you with whatever it lands on..)", default_thumbnail)
    else:
        await game_message(message, "Game failed to start... Please try again later.", default_thumbnail)
