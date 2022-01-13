import json
import argparse
import bots.random.wrapped_client
import os
import logging
import datetime


def __parse__():
    parser = argparse.ArgumentParser(
        description='Random related discord bot.',
    )
    parser.add_argument('CONFIG_FILE', type=str, nargs='?', default='config/config.json', help='Configuration file')
    parser.add_argument('SCRIPTS_FILE', type=str, nargs='?', default='%s/bots/random/services' % script_dir, help='Scripts directory')
    parser.add_argument('LANGUAGUE_FILE', type=str, nargs='?', default='%s/languages/docs.json' % script_dir, help='Languages file')
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

bot = bots.random.wrapped_client.Wrapped_Client(language, scripts_file, prefix=prefix).run(api_key)
