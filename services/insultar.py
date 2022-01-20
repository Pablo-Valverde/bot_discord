import common


@staticmethod
async def __run__(client, message, *args, **kwards):
    mentions = [user for user in message.mentions if not user == client.user]
    if not mentions:
        await common.insultar(message.channel, message.author)
        return
    await common.insultar(message.channel, *mentions)
