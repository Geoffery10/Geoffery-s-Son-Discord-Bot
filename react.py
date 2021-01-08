from re import search

reacts = {
    'rip': "372950049665318925"
}


async def checkReact(message, client):
    if search("(^|\s)r(i|\.)(p|i)(\.|)(p|\s|$)(\.(\s|$)|\s|$)", message.content.lower()):
        print("Reacting RIP")
        await message.add_reaction(r":rip:372950049665318925")
    if search("(^|\s)(stonk)(s|)(\s|$)", message.content.lower()):
        print("Reacting Stonks")
        await message.add_reaction(r":stonks:763100428065046568")
    if search("(^|\s)(cring)(e|y)", message.content.lower()):
        print("Reacting to Cringe")
        await message.add_reaction(r":cringe_harold:763101242728775692")
    if search("(^|\s)(chad)(\s|$)", message.content.lower()):
        print("Reacting to Chad")
        await message.add_reaction(r":Yes_Chad:797139698266406952")
    if search("(^|\s)(to be continued)(\s|$)", message.content.lower()):
        print("Reacting to be continued... Doot doot doot doot <:menacing:797137479705952267>")
        await message.add_reaction(r":to_be_continued:797137298423939153")
    if search("(^|\s)(shrug)(s|ging|\s|$)(\s|$)", message.content.lower()):
        print("Reacting to a shrug.")
        await message.add_reaction(r":Shrug:797140054245638154")
    if search("(^|\s)(f)(\s|$)", message.content.lower()):
        print("Reacting to an F in the chat")
        await message.add_reaction(r":press_F:797137870988640306")
    if search("(^|\s)(pog|pogger)(s(\s|$)|\s|$)", message.content.lower()):
        print("Reacting to a Pog Champ")
        await message.add_reaction(r":pog:797139317071282206")
    if search("(^|\s)(nani|何)(\s|$)", message.content.lower()):
        print("Reacting to a Nani?")
        await message.add_reaction(r":nani:797136854251995186")
    if search("(^|\s)(dio)(\s|$)", message.content.lower()):
        print("Reacting to DIO!!!")
        await message.add_reaction(r":dio:797137020266348615")
    if search("(^|\s)(menacing|dio|scary)(\s|$)", message.content.lower()):
        print("Reacting to a menacing")
        await message.add_reaction(r":menacing:797137479705952267")
    if search("(^|\s)(doubt|press\sx)(\s|$)", message.content.lower()):
        print("Reacting to a doubt")
        await message.add_reaction(r":doubt:797139505437736980")
    if search("(^|\s)(horny|bonk|sauce|sause|hentai)(\s|$)", message.content.lower()):
        print("Bonking react incoming!")
        await message.add_reaction(r":bonk:797139159571628072")
    if search("(^|\s)(report|sus)(\s|$)", message.content.lower()):
        print("Reacting to a report!")
        await message.add_reaction(r":among_us_report:797137767947436043")
    if search("(^|\s)(fbi|f.b.i|f.b.i.)(\s|$)", message.content.lower()):
        print("Reacting to FBI!")
        await message.add_reaction(r":fbi:797174135993532446")
    mentions = message.mentions
    if len(mentions) > 0:
        if mentions[0] == client.user:
            await message.add_reaction('👀')
