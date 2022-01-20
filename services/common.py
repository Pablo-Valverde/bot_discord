import random
import discord
import os


class FileNotFound(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

async def insultar(channel, *args):
    buffer = ""
    for arg in args:
        if not type(arg) == discord.member.Member:
            continue
        buffer += "%s %s\n" % (arg.mention, get_insulto_aleatorio())
    await channel.send(buffer)

def get_insulto_aleatorio():
    if not os.path.isfile("insultos.txt"):
        raise FileNotFound("'insultos.txt' is missing")
    with open("insultos.txt", "rt", encoding="UTF-8") as insultostxt:
        insultos = [insulto.replace("\n","") for insulto in insultostxt.readlines()]
        return random.choice(insultos).lower()
