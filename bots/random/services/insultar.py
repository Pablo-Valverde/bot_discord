import common


@staticmethod
async def __run__(arguments, client, message, *args, **kwards):
    if not arguments:
        return
    arguments = arguments.split(" ", maxsplit=1)[0]
    try:
        member = arguments[3:-1]
        user = await client.fetch_user(int(member))
        if user.id == client.user.id:
            user = message.author
    except:
        user = message.author
    finally:
        await common.insultar(user, message.channel)
        await message.delete()
