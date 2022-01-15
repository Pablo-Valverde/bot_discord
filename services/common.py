import random


async def insultar(user, channel):
        await channel.send("<@!%s> %s" % (user.id, get_insulto_aleatorio()))

def get_insulto_aleatorio():
    with open("insultos.txt", "rt", encoding="UTF-8") as insultostxt:
        insultos = [insulto.replace("\n","") for insulto in insultostxt.readlines()]
        return random.choice(insultos)