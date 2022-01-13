import discord


ping_ranges = {
    65: "🟢",
    200: "🟡",
    9999: "🔴"
}


async def __run__(self, message:discord.Message, client, *args, **kwards):
    ping = client.latency * 100
    buffer = ""
    for ping_value in ping_ranges:
        if ping < ping_value:
            buffer += "%s " % ping_ranges[ping_value]
            break
    buffer += "%.0f ms" % ping
    embed=discord.Embed(title=buffer, color=client.embed_color)
    await message.channel.send(embed=embed)
