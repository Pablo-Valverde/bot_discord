import discord


async def __run__(self, message:discord.Message, client, arguments, *args, **kwards):
    if arguments:
        arguments = arguments.split(" ")
    else:
        arguments = []
    try:
        if arguments.__len__() == 0 or arguments.__len__() > 1:
            raise RuntimeError()
        await show_command_info(message, arguments, client)
    except:
        await show_all_commands(self, message, client)

async def show_all_commands(self, message, client):
    discarded = []
    available_services = client.services
    buffer = ""
    for service in available_services:
        _, service_info = available_services[service]
        if service_info in discarded:
            continue
        buffer += "`%s%s` " % (client.prefix, service_info.name)
        discarded.append(service_info)
    embed=discord.Embed(color=client.embed_color)
    embed.add_field(name=self.name, value=buffer)
    await message.channel.send(embed=embed)

async def show_command_info(message, arguments, client):
    command = arguments[0]
    _, command_info = client.get_available_service(command)
    buffer = "%s\n`%s%s`\n\n**%s**:\n" % (command_info.description, client.prefix, command, client.language["COMMANDS"]["ALIAS"])
    valid_alias = [alias for alias in command_info.aliases if not alias.lower() == command]
    alias = (", ".join(valid_alias)).lower()
    buffer += alias
    embed=discord.Embed(color=client.embed_color)
    embed.add_field(name=command_info.name, value=buffer)
    await message.channel.send(embed=embed)
