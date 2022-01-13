import asyncio
import random
import common


@staticmethod
async def __run__(message, *args, **kwargs):
    members = message.channel.members
    for _ in range(0,10):
        wait_s = random.randint(1,5)
        member = random.choice(members)
        await common.insultar(member, message.channel)
        await asyncio.sleep(wait_s)
