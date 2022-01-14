import random


async def insultar(user, channel):
    with open("insultos.txt", "r") as insultostxt:
        insultos = insultostxt.readlines()
        rand = random.randint(0, insultos.__len__())
        await channel.send("<@!%s> %s" % (user.id, insultos[rand]))
