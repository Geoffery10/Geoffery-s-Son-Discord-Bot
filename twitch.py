import argparse
import os
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError
import json
import requests
from loggingChannel import sendLog
import discord
from dotenv import load_dotenv


async def checkTwitch(users, client):
    for user in users:
        # response = requests.get(f'https://api.twitch.tv/{user}/channels', headers=headers, params=params)
        user["id"] = await check_user(user, client)

    return users


async def check_user(user, client):
    Client_ID = os.getenv('TWITCH_CLIENT_ID')
    Client_Secret = os.getenv('TWITCH_CLIENT_SECRET')
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': Client_ID,
    }
    params = (
        ('login', user['name']),
    )
    response = requests.get('https://api.twitch.tv/kraken/users', headers=headers, params=params)
    json_response = response.json()

    status = json_response['users'][0]

    response = requests.get('https://api.twitch.tv/helix/', headers=headers)

    params = (
        ('client_id', Client_ID),
        ('client_secret', Client_Secret),
        ('grant_type', 'client_credentials'),
    )

    token = requests.post('https://id.twitch.tv/oauth2/token', params=params)
    token = token.json()['access_token']
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-ID': Client_ID
    }
    params = (
        ('query', user['name']),
    )

    response = requests.get('https://api.twitch.tv/helix/search/channels', headers=headers, params=params)

    """ returns 0: online, 1: offline, 2: not found, 3: error """
    info = response.json()['data'][0]
    try:
        if info['is_live'] is False:
            status = f"1: {info['display_name']} offline"
        else:
            if not user["id"] == info['id']:
                print(await sendLog(f'id: {user["id"]} new id: {info["id"]}', client))
                user["id"] = info["id"]
                print(await sendLog(f"0: {info['display_name']} online playing {info['game_name']}.\n{info}", client))
                channel = client.get_channel(483867465613443082)
                embed = discord.Embed(title=info["title"], colour=discord.Colour(0x9147ff),
                                      url=f"https://www.twitch.tv/{info['broadcaster_login']}",
                                      description=f"{info['display_name']} is streaming {info['game_name']}",
                                      timestamp=datetime.strptime(info['started_at'], "%Y-%m-%dT%H:%M:%SZ"))

                embed.set_image(
                    url=info['thumbnail_url'])
                embed.set_author(name="Twitch", url=f"https://www.twitch.tv/{info['broadcaster_login']}",
                                 icon_url="https://cdn4.iconfinder.com/data/icons/social-media-square-4/1024/square-11-512.png")
                embed.set_footer(text="Twitch", icon_url="https://assets.help.twitch.tv/Glitch_Purple_RGB.png")
                await channel.send(embed=embed)
                return user["id"]
    except URLError as e:
        if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
            print(await sendLog(f"2: {user} not found", client))
        else:
            print(await sendLog(f"3: {user} error", client))

    return user["id"]
