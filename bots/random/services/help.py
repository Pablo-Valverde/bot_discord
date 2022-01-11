import discord

async def execute(**kwards):
    await __func(message=kwards["message"], client=kwards["client"], command=kwards["command"], arguments=kwards["arguments"])

async def __func(message:discord.Message, client, command, arguments):
    commands = client.language["COMMANDS"]
    embed = None
    try:
        if arguments.__len__() == 1:
            requested_command = arguments[0].lower()
            command_info = commands[requested_command.upper()]
            embed = await __args_get_embed(client, command, command_info)
        else:
            assert False
    except (AssertionError, KeyError):
        embed = await __no_args_get_embed(client, command, commands)
    await message.channel.send(embed=embed)

async def __args_get_embed(client, main_command, command_info):
    name = command_info["NAME"]
    long_description = command_info["LONG_DESCRIPTION"]
    permission = client.language["PERMISSIONS"][command_info["PERMISSIONS_REQUIRED"].__str__()]
    usage = "`%s%s`" % (client.prefix, name)
    return discord.Embed(
        title="%s command: %s" % (main_command,name),
        description="%s\n%s: **%s**\n\n%s" % (usage,client.language["PERMISSIONS_REQUIRED"],permission,long_description), 
        color=0xffdfa8
        )

async def __no_args_get_embed(client, main_command, commands):
    available_commands = ""
    for command_key in commands:
        name = commands[command_key]["NAME"]
        available_commands += "`%s%s` " % (client.prefix, name)
    return discord.Embed(
        title="%s command" % main_command, 
        description=available_commands, 
        color=0xffdfa8
        )
