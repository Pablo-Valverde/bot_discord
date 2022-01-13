import random
import discord


ping_ranges = {
    65: "🟢",
    200: "🟡",
    9999: "🔴"
}

async def insultar(user, channel):
    with open("insultos.txt", "r") as insultostxt:
        insultos = insultostxt.readlines()
        rand = random.randint(0, insultos.__len__())
        await channel.send("<@!%s> %s" % (user.id, insultos[rand]))

async def ping(channel, client):
    ping = client.latency * 100
    buffer = ""
    for ping_value in ping_ranges:
        if ping < ping_value:
            buffer += "%s " % ping_ranges[ping_value]
            break
    buffer += "%.0f ms" % ping
    embed=discord.Embed(title=buffer, color=client.embed_color)
    await channel.send(embed=embed)
