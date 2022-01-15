import asyncio
import random
import common
import discord
from random import shuffle


running = False

@staticmethod
async def __run__(message, client, *args, **kwargs):
    global running
    if running:
        return
    running = True
    members = [
        member for member in message.channel.members 
        if
            (member.status == discord.Status.online) 
            and (not member.id == client.user.id)
    ]
    if not members:
        embed = discord.Embed(
            title=client.no_users,
            color=client.embed_color_error
        )
        await message.channel.send(embed=embed)
        return
    shuffle(members)
    for member in members:    
        wait_s = random.random()*2
        await common.insultar(member, message.channel)
        if not members.index(member) == members.__len__() - 1:
            await message.channel.trigger_typing()
            await asyncio.sleep(wait_s)
    running = False
