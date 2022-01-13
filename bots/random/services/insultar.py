async def __run__(self, arguments, client, message, *args, **kwards):
        if not arguments:
                return
        arguments = arguments.split(" ", maxsplit=1)[0]
        member = arguments[3:-1]
        await insult_member(member, message.channel, client, message.author.id)

async def insult_member(id, channel, client, self_id):
    import random
    rand = random.randint(0, client.insultos.__len__())
    if id.__str__() == client.user.id.__str__():
        await channel.send("<@!%s> %s" % (self_id, client.insultos[rand]))
        return
    user = await client.fetch_user(id)
    await channel.send("<@!%s> %s" % (user.id, client.insultos[rand]))