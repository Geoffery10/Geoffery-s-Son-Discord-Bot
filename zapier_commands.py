import json
from datetime import datetime, timezone
from re import search
import discord
from discord import user
from loggingChannel import sendLog


async def commands(message, client):
    channel = client.get_channel(756745560416845884)
    user = client.get_user(253710834553847808)

    if search("instagram", message.content.lower()):
        end = len(message.content) - 3
        message.content = message.content[3:end]
        # print(await sendLog(log=f'Cleaned Zapier Message: {message.content}', client=client))
        zapier_dic = eval(message.content)
        dt = datetime.strptime(zapier_dic['Timestamp'], '%Y-%m-%dT%H:%M:%S%z')
        timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

        description = f"{zapier_dic['Caption']}"
        if zapier_dic['Media_Type'] == 'VIDEO':
            description = f"{zapier_dic['Caption']}\n\nWATCH HERE -> {zapier_dic['Permalink']}"
        # print(await sendLog(log=f'Timestamp: {zapier_dic["Timestamp"]} -> {dt.strftime("%Y-%m-%d-T%H:%M:%S.%z")}', client=client))
        embed = discord.Embed(title=f"{zapier_dic['Username']}", colour=discord.Colour(0xd23363), url=f"{zapier_dic['Permalink']}", description=description,
                              timestamp=datetime.utcfromtimestamp(timestamp))
        if zapier_dic['Media_Type'] == 'IMAGE':
            embed.set_image(url={zapier_dic['Media_URL']})
        embed.set_thumbnail(url=f"{zapier_dic['Thumbnail URL']}")
        embed.set_author(name=f"{user.display_name}", url="https://www.instagram.com/geoffery10/",
                         icon_url=f"{user.avatar_url}")
        embed.set_footer(text="Instagram",
                         icon_url="https://chaminade.edu/wp-content/uploads/2019/08/Instagram-Icon-color.png")

        await channel.send(embed=embed)
