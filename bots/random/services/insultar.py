import random

        
async def __run__(self, arguments, client, message, *args, **kwards):
    print(arguments, client, message)
    if not arguments:
        return
    arguments = arguments.split(" ", maxsplit=1)[0]
    try:
        member = arguments[3:-1]
        user = await client.fetch_user(int(member))
        if user.id == client.user.id:
            user = message.author
    except:
        user = message.author
    finally:
        await insult_member(user, message.channel)

async def insult_member(user, channel):
    with open("insultos.txt", "r") as insultostxt:
        insultos = insultostxt.readlines()
        rand = random.randint(0, insultos.__len__())
        await channel.send("<@!%s> %s" % (user.id, insultos[rand]))