import asyncio
import random
import common
import discord


@staticmethod
async def __run__(message, client, *args, **kwargs):
    members = [
        member for member in message.channel.members 
        if
            (member.status == discord.Status.online or member.status == discord.Status.idle) 
            and (not member.id == client.user.id)
    ]
    if not members:
        embed = discord.Embed(
            title=client.no_users,
            color=client.embed_color_error
        )
        await message.channel.send(embed=embed)
        return
    embed = discord.Embed(
            title="AaAaAAaaaaAaAaaaAAAah!!1!!!11",
            color=client.embed_color_error
        )
    await message.channel.send(embed=embed)
    for _ in range(0,10):    
        wait_s = random.randint(1,5)
        member = random.choice(members)
        await common.insultar(member, message.channel)
        await asyncio.sleep(wait_s)
