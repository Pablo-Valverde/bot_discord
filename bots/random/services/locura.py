from ast import arguments
import asyncio
import random


is_running = False

async def __run__(self, *args, **kwards):
    global is_running
    if is_running:
        is_running = False
        return
    is_running = True
    try:
        asyncio.run_coroutine_threadsafe(await completamente_batracio(*args, **kwards))
        asyncio.run_coroutine_threadsafe(await cambiar_titulo(*args, **kwards))
    except TypeError:
        pass

async def completamente_batracio(message, client, *args, **kwards):
    insultar, _ = client.get_available_service("insultar")
    members = message.guild.members
    while True:
        wait = random.randint(1, 5)
        rand = random.randint(0, members.__len__()-1)
        member_id = members[rand].id
        await insultar(arguments="", client=client, message=message, *args, **kwards)
        await asyncio.sleep(wait)

async def cambiar_titulo(message, *args, **kwards):
    guild = message.guild
    nombres = ["🙉🍌ⒶⓊⓉⒾⓈⓉ🤡🎈", "🎈🙉ⒶⓊⓉⒾⓈⓉ🍌🤡", "🤡🎈ⒶⓊⓉⒾⓈⓉ🙉🍌", "🍌🤡ⒶⓊⓉⒾⓈⓉ🎈🙉", "🙉🍌ⒶⓊⓉⒾⓈⓉ🤡🎈"]
    try:
        while is_running:
            nombre = nombres.pop(0)
            nombres.append(nombre)
            await guild.edit(name=nombre)
            await asyncio.sleep(1)
    except:
        pass
