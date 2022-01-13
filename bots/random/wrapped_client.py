from . import _service
import discord
import logging


class Wrapped_Client(discord.Client):

    def __init__(self, language : dict, services_path : str, prefix : str="", logger : logging.Logger=logging.getLogger('bot_client')) -> None:
        intent = discord.Intents.all()
        super().__init__(intents=intent)
        self.language = language
        self.prefix = prefix
        self.logger = logger
        self.embed_color = int(self.language["EMBED_COLOR_CORRECT"],16)
        self.embed_color_error = int(self.language["EMBED_COLOR_ERROR"],16)
        error_title = self.language["COMMANDS"]["ERROR_TITLE"]
        error_msg = self.language["COMMANDS"]["COMMAND_ERROR"]
        embed=discord.Embed(color=self.embed_color_error)
        embed.add_field(name=error_title, value=error_msg)
        self.embed_error = embed
        _service.load_services(services_path, self.language["COMMANDS"]["AVAILABLE_COMMANDS"])
        self.services = _service.services

    def get_available_service(self, name):
        return _service.get_service(name)

    def parse_message(self, message:discord.Message):
        message_splited = message.content.split(" ", maxsplit=1)
        if message_splited.__len__() <= 0:
                return None
        unf_command = message_splited[0]
        f_command = unf_command
        if self.prefix:
                f_command = unf_command[1:] if unf_command[0] == self.prefix else None
        if not f_command:
                return None
        f_arguments = ""
        if message_splited.__len__() > 1:
                f_arguments = message_splited[1]
        return (f_command, f_arguments)

    async def on_ready(self):
        self.logger.info('Bot is ready.')

    async def on_message(self, message:discord.Message):
        if not message.content: return
        if not self.is_ready(): return
        parsed_message = self.parse_message(message)
        if not parsed_message: return
        command, argument = parsed_message
        self.logger.info('"%s" by %d on channel %d of guild %d.' % (message.content, message.author.id, message.channel.id, message.guild.id))
        await self.get_service(command, message=message, client=self, arguments=argument)

    async def get_service(self, service_name, **options):
        try:
            code, _ = _service.get_service(service_name.lower())
            await code(**options)
        except _service.ServiceNotFound:
            pass
        except:
            message=options["message"]
            await message.channel.send(embed=self.embed_error)
