from re import search

reacts = {
    'rip': "372950049665318925"
}


async def checkReact(message, client):
    if search("(^|\s)r(i|.)(p|i)(.|)(p|)", message.content.lower()):
        print("Reacting RIP")
        await message.add_reaction(r":rip:372950049665318925")
