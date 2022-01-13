from os import stat
import common


@staticmethod
async def __run__(message, client, *args, **kwards):
    await common.ping(message.channel, client)
