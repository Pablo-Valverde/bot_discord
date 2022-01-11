import discord

async def execute(**kwards):
    await __func(message=kwards["message"], client=kwards["client"])

async def __func(message:discord.Message, client):
    ping = client.latency * 100
    await message.channel.send("%.0f ms" % ping)
