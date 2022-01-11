import discord
import json
import argparse
import logging
import datetime
import enum

class language(enum.Enum):

    ES = "ES"

    def __str__(self) -> str:
        return self.name

def parse():
    parser = argparse.ArgumentParser(
        description='Random related discord bot.',
    )
    parser.add_argument('CONFIG_FILE', type=str, nargs='?', default='config/config.json', help='Configuration file')
    parser.add_argument('LANGUAGE', type=language, nargs='?', default="ES",choices=list(language))
    return parser.parse_args()

args = parse()
CONFIG_FILE = args.CONFIG_FILE

init_time = datetime.datetime.now()
config = json.load(open(CONFIG_FILE))

log_directory = config['LOG_DIRECTORY']
log_extension = config['LOG_FILE_EXT'].replace('.', '')

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
log_file = '%s/%s.%s' % (log_directory, init_time.strftime('%Y-%m-%d_%H-%M'), log_extension)
handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='w+')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Wrapped_Client(discord.Client):

    def __init__(self, prefix=None, language=language.ES) -> None:
        super().__init__()
        self.language = json.load(open("languages/docs.json"))[language.__str__()]
        self.prefix = prefix

    def parse_command(self, message:discord.Message):
        individual_messages = message.content.split(" ", maxsplit=1)
        command = individual_messages[0]
        arguments = individual_messages[1].split(" ") if individual_messages.__len__() > 1 else []
        return (command[1:], arguments) if command[0] == self.prefix else (None, None)

    async def on_ready(self):
        logger.info('Bot is ready.')

    async def on_message(self, message:discord.Message):
        if not message.content: return
        if not self.is_ready(): return
        command, arguments = self.parse_command(message)
        if not command: return
        logger.info('"%s" by %d on channel %d of guild %d.' % (message.content, message.author.id, message.channel.id, message.guild.id))
        await self.get_service(command, arguments, message=message)

    async def get_service(self, service_name, arguments, **options):
        """
            Partially from:
            #https://www.geeksforgeeks.org/how-to-dynamically-load-modules-or-classes-in-python/

            Get a service from services folder, dynamically loaded and
            execute it.

            Available options:
            message: discord.Message

        """
        service_name = service_name.lower()
        service_name = service_name.replace("_", "")
        try:
            #__import__ method used
            # to fetch module
            module = __import__("services.%s" % service_name)
            # getting execute by
            # getattr() method
            await getattr(module, service_name).execute(**options, client=self, command=service_name, arguments=arguments)
        except ModuleNotFoundError as mnfe:
            # TODO log error 
            pass

bot = Wrapped_Client(prefix='-').run(config['BOT_KEY'])
