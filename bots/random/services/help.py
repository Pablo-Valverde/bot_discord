import discord

async def execute(**kwards):
    await __func(message=kwards["message"], client=kwards["client"])

async def __func(message:discord.Message, client):
    await message.channel.send(client.language["HELP_COMMAND"])
