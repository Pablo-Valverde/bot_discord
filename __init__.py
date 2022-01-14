import json
import argparse
import pydiscord
import os
import logging
import datetime
import discord


def __parse__():
    parser = argparse.ArgumentParser(
        description='Random related discord bot.',
    )
    parser.add_argument('CONFIG_FILE', type=str, nargs='?', default='config/config.json', help='Configuration file')
    parser.add_argument('SCRIPTS_FILE', type=str, nargs='?', default='services', help='Scripts directory')
    parser.add_argument('LANGUAGUE_FILE', type=str, nargs='?', default='languages/docs.json', help='Languages file')
    languages = json.load(open(parser.parse_args().LANGUAGUE_FILE))
    available_languages = [language for language in languages]
    parser.add_argument('LANGUAGE', type=str, nargs='?', default="ES", choices=available_languages)
    return parser.parse_args()

script_dir = os.path.dirname(__file__)
args = __parse__()

init_time = datetime.datetime.now()
config = json.load(open(args.CONFIG_FILE))
language = json.load(open(args.LANGUAGUE_FILE))[args.LANGUAGE]

log_directory = config['LOG_DIRECTORY']
log_extension = config['LOG_FILE_EXT'].replace('.', '')
prefix = config['PREFIX']

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
log_file = '%s/%s.%s' % (log_directory, init_time.strftime('%Y-%m-%d_%H-%M'), log_extension)
handler = logging.FileHandler(filename="%s/%s" % (script_dir,log_file), encoding='utf-8', mode='w+')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

api_key = config['BOT_KEY']
scripts_file = args.SCRIPTS_FILE

class felaciano(pydiscord.Wrapped_Client):

    def __init__(self, language: dict, services_path: str, prefix: str = "", logger: logging.Logger = None) -> None:
        super().__init__(language, services_path, prefix, logger)

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
        activity = discord.Activity(type=discord.ActivityType.watching, name="el porn channel")
        await self.change_presence(activity=activity)
        self.logger.info('Bot is ready.')
    
    async def on_message(self, message:discord.Message):
        if not message.content: return
        if not self.is_ready(): return
        parsed_message = self.parse_message(message)
        if not parsed_message: return
        command, argument = parsed_message
        self.logger.info('"%s" by %d on channel %d of guild %d.' % (message.content, message.author.id, message.channel.id, message.guild.id))
        await self.execute_service(command, message=message, client=self, arguments=argument)

bot = felaciano(language, scripts_file, prefix=prefix).run(api_key)