import json
import os
from loggingChannel import sendLog

client = ""


async def get_member_data(update_client):
    global client
    client = update_client
    with open('memberData/memberData.json', 'r') as f:
        data = json.load(f)
        return data


async def store_member_data(data):
    filename = "memberData/memberData.json"
    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(await sendLog(log=f'Saved new member data to json.', client=client))


async def search_member_data(data, newvalue, member):
    found = False
    for value in data:
        if newvalue == value['userID']:
            found = True
            print(await sendLog(log=f'Member is already in database.', client=client))
    if not found:
        data = await add_member_data(data, member)
    return data


async def add_member_data(data, member):
    new_user_dict = {
        'user': member.name,
        'userID': member.id,
        'sins': 'Sinless... for now...',
        'score': 0
    }
    print(await sendLog(log=(f'New member added to memberData: {new_user_dict}'), client=client))
    data.append(new_user_dict)
    await store_member_data(data)
    return data
