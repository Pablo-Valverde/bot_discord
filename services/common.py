import random
import os


class FileNotFound(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

async def insultar(user, channel):
        await channel.send("<@!%s> %s" % (user.id, get_insulto_aleatorio()))

def get_insulto_aleatorio():
    if not os.path.isfile("insultos.txt"):
        raise FileNotFound("'insultos.txt' is missing")
    with open("insultos.txt", "rt", encoding="UTF-8") as insultostxt:
        insultos = [insulto.replace("\n","") for insulto in insultostxt.readlines()]
        return random.choice(insultos).lower()
