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


def _data_path(*parts):
    """Resolve a path under $BOT_DATA_DIR (default: bot's working dir)."""
    return os.path.join(os.environ.get('BOT_DATA_DIR', '.'), *parts)


async def fixNick(member):
    if member.nick == None or member.nick == "None":
        return member.name
    return member.nick


def _game_file_path():
    """Path to the Russian Roulette persistent game state file."""
    return _data_path('gameData', 'Russian Roulette', 'games.json')


def ensure_game_file():
    """Create the Russian Roulette data directory/file if missing.

    The file is runtime state and is gitignored, so fresh deploys/LXC rebuilds
    may not have it. Slash commands should self-heal instead of failing.
    """
    game_file = _game_file_path()
    os.makedirs(os.path.dirname(game_file), exist_ok=True)
    if not path.exists(game_file):
        with open(game_file, "w") as write_file:
            json.dump([], write_file, indent=4)


async def acknowledge_interaction(interaction):
    """Acknowledge a slash interaction before posting public game embeds."""
    if not interaction.response.is_done():
        await interaction.response.defer(ephemeral=True)


async def check_game_file():
    ensure_game_file()
    return path.exists(_game_file_path())


async def get_game_data():
    ensure_game_file()
    with open(_game_file_path(), "r") as read_file:
        game_data_set = json.load(read_file)
    return game_data_set


async def save_game_data(game_data_set, interaction):
    """Create a new game in the channel where the slash command was invoked."""
    new_game = {
        "guild": interaction.guild.id,
        "channel": interaction.channel.id,
        "active": True,
        "players": [interaction.user.id],
        "bullet_index": randint(1, 6),
        "current_index": 1
    }
    game_data_set.append(new_game)
    print("Creating new game data")
    with open(_game_file_path(), "w") as write_file:
        json.dump(game_data_set, write_file, indent=4)


async def update_game_data(game_data_set, new_data):
    print("Updating game data")
    index = 0
    for index in range(len(game_data_set)):
        if game_data_set[index]["channel"] == new_data["channel"]:
            game_data_set[index] = new_data
            print("Found Data to Update")
    with open(_game_file_path(), "w") as write_file:
        json.dump(game_data_set, write_file, indent=4)


async def check_for_game(interaction, game_data_set):
    """Look up a game in the channel the slash command was invoked in."""
    data = {}
    game_found = False
    for data_set in game_data_set:
        if str(data_set["channel"]) == str(interaction.channel.id):
            print("Game found on this channel")
            game_found = True
            data = data_set
            break
    return game_found, data


async def game_message(interaction, description, thumbnail):
    embed = discord.Embed(title="Russian Roulette", colour=discord.Colour(0x69645f), url="http://government.ru/en/",
                          description=description)
    embed.set_thumbnail(
        url=thumbnail)
    embed.set_author(name="Vladimir Putin", url="http://government.ru/en/",
                     icon_url="https://media.vanityfair.com/photos/5874192bee23284912086649/1:1/w_960,h_960,"
                              "c_limit/vladimir-putin-evil.jpg")
    await interaction.channel.send(embed=embed)


async def shoot(interaction, client):
    await acknowledge_interaction(interaction)
    nick = await fixNick(interaction.user)
    if await check_game_file():
        print("GAME DATA FOUND")
        game_data_set = await get_game_data()
        game_found, data = await check_for_game(interaction, game_data_set)
        if game_found:
            if data["active"]:
                if data["current_index"] == data["bullet_index"]:
                    data["active"] = False
                    await game_message(interaction, f"<:rip:372950049665318925> {nick} you will be missed...",
                                       interaction.user.display_avatar.url)
                else:
                    data["current_index"] += 1
                    if data["current_index"] > 6:
                        data["current_index"] = 1
                    await game_message(interaction, f"Seems you get to live today {nick}...", interaction.user.display_avatar.url)
                if interaction.user.id not in data["players"]:
                    data["players"].append(interaction.user.id)
                await update_game_data(game_data_set, data)
            else:
                await startGame(interaction, client)
        else:
            await startGame(interaction, client)
    else:
        await game_message(interaction, "Game failed to start... Please try again later.", default_thumbnail)


async def spin(interaction, client):
    await acknowledge_interaction(interaction)
    nick = await fixNick(interaction.user)
    if await check_game_file():
        print("GAME DATA FOUND")
        game_data_set = await get_game_data()
        game_found, data = await check_for_game(interaction, game_data_set)
        if game_found:
            if data["active"]:
                data["current_index"] = randint(1, 6)
                if data["current_index"] == data["bullet_index"]:
                    data["active"] = False
                    await game_message(interaction,
                                       f"<:rip:372950049665318925> {nick} you will be missed...",
                                       interaction.user.display_avatar.url)
                else:
                    data["current_index"] += 1
                    if data["current_index"] > 6:
                        data["current_index"] = 0
                    await game_message(interaction, f"Seems you get to live today {nick}...",
                                       interaction.user.display_avatar.url)
                if interaction.user.id not in data["players"]:
                    data["players"].append(interaction.user.id)
                await update_game_data(game_data_set, data)
            else:
                await startGame(interaction, client)
        else:
            await startGame(interaction, client)
    else:
        await game_message(interaction, "Game failed to start... Please try again later.", default_thumbnail)


async def startGame(interaction, client):
    # Acknowledge the slash command first so Discord doesn't show "interaction failed"
    await acknowledge_interaction(interaction)
    if not interaction.response.is_done():
        await interaction.followup.send("Starting Russian Roulette...", ephemeral=True)

    if await check_game_file():
        print("GAME DATA FOUND")
        game_data_set = await get_game_data()
        game_found, data = await check_for_game(interaction, game_data_set)
        if game_found:
            await game_message(interaction, "Starting Game... Use /shoot to shoot and /spin to spin. (Note spin "
                                        "will also shoot you with whatever it lands on..)", default_thumbnail)
            new_data = {
                "guild": interaction.guild.id,
                "channel": interaction.channel.id,
                "active": True,
                "players": [interaction.user.id],
                "bullet_index": randint(1, 6),
                "current_index": 1
            }
            await update_game_data(game_data_set, new_data)
        else:
            print("No game was found for this channel")
            await save_game_data(game_data_set, interaction)
            await game_message(interaction, "Starting Game... Use /shoot to shoot and /spin to spin. (Note spin "
                                        "will also shoot you with whatever it lands on..)", default_thumbnail)
    else:
        await game_message(interaction, "Game failed to start... Please try again later.", default_thumbnail)
