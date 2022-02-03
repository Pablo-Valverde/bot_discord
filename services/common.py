import discord
import requests


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
    request = requests.get("http://127.0.0.1/insultos/aleatorio")
    request_json = request.json()
    try:
        value = request_json["data"]["value"]
        return value
    except KeyError:
        return "No tengo insultos para decirte"
