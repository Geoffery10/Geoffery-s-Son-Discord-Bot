from re import search

reacts = {
    'rip': "372950049665318925"
}


async def checkReact(message, client):
    if search("(^|\s)r(i|\.)(p|i)(\.|)(p|)", message.content.lower()):
        print("Reacting RIP")
        await message.add_reaction(r":rip:372950049665318925")
    if search("(^|\s)(stonk)(s|)", message.content.lower()):
        print("Reacting Stonks")
        await message.add_reaction(r":stonks:763100428065046568")
    if search("(^|\s)(cring)(e|y)", message.content.lower()):
        print("Reacting to Cringe")
        await message.add_reaction(r":cringe_harold:763101242728775692")
