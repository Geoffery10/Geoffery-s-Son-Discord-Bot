import discord
from mcstatus import JavaServer
from loggingChannel import sendLog
import requests
import json
import os
from dotenv import load_dotenv


async def ping_MC_server(client, message):
    IP = os.getenv('MC_DNS')
    PORT = os.getenv('MC_PORT')
    RCON_PASSWORD = os.getenv('MC_RCON_PASS')
    # with MCRcon(f"{IP}:{PORT}", RCON_PASSWORD) as mcr:
        # resp = mcr.command("/ip")
        # print(resp)

    # Get IP
    url = "https://api.ipify.org/?format=json"
    ip = "error"
    r = requests.get(url)
    if r.status_code == 200:
        ip = json.loads(r.content)
        ip_address = ip["ip"]
        print(f'IP: {ip_address}')
        server = JavaServer.lookup(f"{ip_address}:{str(PORT)}")
        print(f"JavaServer.lookup({ip_address}:{str(PORT)}")
    else:
        server = JavaServer.lookup(f"{IP}:{str(PORT)}")
        print(f"JavaServer.lookup({IP}:{str(PORT)})")

    serverOnline = True
    queryPass = False
    try:
        status = server.status()
        print(f"Status: {status}")
    except Exception:
        serverOnline = False
        print(f"Status: Failed")

    try:
        query = server.query()
        print(f"Query: {query}")
        queryPass = True
    except Exception:
        print(f"Quary: Failed")

    if serverOnline:
        imageURL = "https://minecraft-statistic.net/img/screen/icon/167506.png"
    else:
        imageURL = "https://media.minecraftforum.net/attachments/300/619/636977108000120237.png"

    # Create Embed
    if queryPass:
        description = f"**IP**: {IP}:{PORT}\n**MOTD**: {query.raw.get('hostname')}"
    else:
        description = f"**IP**: {IP}:{PORT}"
    embed = discord.Embed(title="Minecraft Server", colour=discord.Colour(0x63a121), url="https://discordapp.com", description=description)
    if serverOnline:
        print(await sendLog(log=f'{server.status}', client=client))
        embed.add_field(name="Status", value=":green_circle: Online")
        embed.add_field(name="Player Count", value=f"{status.players.online}/{status.raw.get('players').get('max')}")
        if queryPass:
            embed.add_field(name="Version", value=f"{query.raw.get('version')}")
            onlinePlayers = "{0}".format(", ".join(query.players.names))
            if len(onlinePlayers) > 0:
                embed.add_field(name="Players", value=f"{onlinePlayers}")
            else:
                embed.add_field(name="Players", value=f"<:press_F:797137870988640306> None")
        if len(status.raw.get('modinfo')) > 0:
            embed.add_field(name="Modded", value=f"True")
    else:
        embed.add_field(name="Status", value=":red_circle: Offline")
    embed.set_thumbnail(url=imageURL)
    embed.set_author(name="Geoffery10", icon_url="https://static.planetminecraft.com/files/avatar/918830_1.png")
    
    await message.channel.send(embed=embed)


async def ping_MC_server_ctx(client, ctx):
    IP = os.getenv('MC_DNS')
    PORT = os.getenv('MC_PORT')
    RCON_PASSWORD = os.getenv('MC_RCON_PASS')
    # with MCRcon(f"{IP}:{PORT}", RCON_PASSWORD) as mcr:
    # resp = mcr.command("/ip")
    # print(resp)

    # Get IP
    url = "https://api.ipify.org/?format=json"
    ip = "error"
    r = requests.get(url)
    if r.status_code == 200:
        ip = json.loads(r.content)
        ip_address = ip["ip"]
        print(f'IP: {ip_address}')
        server = JavaServer.lookup(f"{ip_address}:{str(PORT)}")
        print(f"JavaServer.lookup({ip_address}:{str(PORT)}")
    else:
        server = JavaServer.lookup(f"{IP}:{str(PORT)}")
        print(f"JavaServer.lookup({IP}:{str(PORT)})")

    serverOnline = True
    queryPass = False
    try:
        status = server.status()
        print(f"Status: {status}")
    except Exception:
        serverOnline = False
        print(f"Status: Failed")

    try:
        query = server.query()
        print(f"Query: {query}")
        queryPass = True
    except Exception:
        print(f"Quary: Failed")

    if serverOnline:
        imageURL = "https://minecraft-statistic.net/img/screen/icon/167506.png"
    else:
        imageURL = "https://media.minecraftforum.net/attachments/300/619/636977108000120237.png"

    # Create Embed
    if queryPass:
        description = f"**IP**: {IP}:{PORT}\n**MOTD**: {query.raw.get('hostname')}"
    else:
        description = f"**IP**: {IP}:{PORT}"
    embed = discord.Embed(title="Minecraft Server", colour=discord.Colour(0x63a121), url="https://discordapp.com",
                          description=description)
    if serverOnline:
        print(await sendLog(log=f'{server.status}', client=client))
        embed.add_field(name="Status", value=":green_circle: Online")
        embed.add_field(name="Player Count", value=f"{status.players.online}/{status.raw.get('players').get('max')}")
        if queryPass:
            embed.add_field(name="Version", value=f"{query.raw.get('version')}")
            onlinePlayers = "{0}".format(", ".join(query.players.names))
            if len(onlinePlayers) > 0:
                embed.add_field(name="Players", value=f"{onlinePlayers}")
            else:
                embed.add_field(name="Players", value=f"<:press_F:797137870988640306> None")
        if len(status.raw.get('modinfo')) > 0:
            embed.add_field(name="Modded", value=f"True")
    else:
        embed.add_field(name="Status", value=":red_circle: Offline")
    embed.set_thumbnail(url=imageURL)
    embed.set_author(name="Geoffery10", icon_url="https://static.planetminecraft.com/files/avatar/918830_1.png")

    await ctx.send(embed=embed)