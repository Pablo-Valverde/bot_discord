#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
from time import sleep
from PIL import Image,ImageFont,ImageDraw,ImageOps
import json
import argparse
import random
import sys
import services.common
import pydiscord
import os
import logging
import datetime
import discord


EXIT_TIME = 10

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
if not os.path.isdir(log_directory):
    if not os.path.exists(log_directory):
        logger.info("Created directory '%s'" % log_directory)
        os.mkdir(log_directory)
    else:
        logger.error("'%s' is a file, not a directory for the logs." % log_directory)
        print("'%s' is a file, not a directory for the logs. exiting in %d seconds..." % (log_directory,EXIT_TIME))
        sleep(EXIT_TIME)
        exit()

handler = logging.FileHandler(filename="%s/%s" % (script_dir,log_file), encoding='utf-8', mode='w+')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

api_key = config['BOT_KEY']
scripts_file = args.SCRIPTS_FILE
if not os.path.isdir(scripts_file):
    logger.error("'%s' is not a directory. Check if it exists." % scripts_file)
    print("'%s' is not a valid scripts directory. exiting in %d seconds..." % (scripts_file,EXIT_TIME))
    sleep(EXIT_TIME)
    exit()

welcome_memebrs = config['ON_MEMBER_JOIN']['ENABLED']
insult = config['ON_MEMBER_JOIN']['INSULT']

connect_channels = config['ON_VOICE_STATE_UPDATE']['ENABLED']
prob = config['ON_VOICE_STATE_UPDATE']['CHANCE']

class felaciano(pydiscord.Wrapped_Client):

    def __init__(self, services_path: str, prefix: str = "", language: dict = None, logger: logging.Logger = None, connect = True, welcome = True, insult = True, join_chance = 0.02) -> None:
        super().__init__(services_path, prefix=prefix, language=language, logger=logger)
        if not os.path.isdir("resources"):
            if not os.path.exists("resources"):
                logger.info("Created directory 'resources'")
                os.mkdir("resources")
            else:
                logger.warning("'resources' should be a directory")
        if os.path.isdir("resources"):
            if not os.path.isdir("resources/respiraciones/"):
                if not os.path.exists("resources/respiraciones/"):
                    logger.info("Created directory 'resources/respiraciones/'")
                    os.mkdir("resources/respiraciones/")
                else:
                    logger.warning("'resources/respiraciones/' should be a directory")
        self.sound_channel = None
        self.connect_channels = connect
        self.prob = join_chance
        self.welcome_members = welcome
        self.insult = insult

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="el porn-channel")
        await self.change_presence(activity=activity)
        self.logger.info('Bot is ready.')
    
    async def on_message(self, message:discord.Message):
        if message.author.bot: return
        if not self.is_ready():
            await message.channel.send("Pero subnormal, dejame llegar al ordenador al menos.")
            return
        await self.welcome(message.author)
        await super().on_message(message)

    async def on_error(self, event_method, *args, **kwargs):
        e = sys.exc_info()[1]
        logger.error(e)
        print("%s non-fatal exception" % e)

    async def on_voice_state_update(self, member, before, after):
        if not self.connect_channels: return
        if member.bot: return
        if not after.channel: return
        channel = after.channel
        if not channel: return
        roll = random.randint(1,100)
        if roll <= int(self.prob * 100):
            if self.voice_clients:
                await self.voice_clients[0].disconnect()
            await channel.connect()
            self.sound_channel = discord.utils.get(self.voice_clients, guild = channel.guild)
            if not os.path.isdir("resources/respiraciones/"):
                self.logger.warning("'resources/respiraciones/' is missing, create it or the bot will only join silently...")
                return
            scripts_on_dir = os.listdir("resources/respiraciones/")
            sounds_on_dir = [f for f in scripts_on_dir if (os.path.isfile(os.path.join("resources/respiraciones/", f)) and f.find(".mp3") > -1)]
            if sounds_on_dir.__len__() == 0:
                self.logger.warning("'resources/respiraciones/' got no .mp3 files, add some so the bot can play sound, joinning silently...")
                return
            sound = random.choice(sounds_on_dir)
            self.sound_channel.play(discord.FFmpegPCMAudio("resources/respiraciones/%s" % sound))

    async def welcome(self, member):
        channel = member.guild.system_channel
        if not channel:
            return
        member_bytes = await member.avatar_url.read()

        circle_white = Image.new('RGBA', (1024, 1024), (255, 0, 0, 0))
        border = ImageDraw.Draw(circle_white)
        border.ellipse([(0,0),(1024,1024)], fill="white", outline="white")
        member_photo = Image.open(io.BytesIO(member_bytes))
        mask = Image.open("resources/mask.png").convert("L")
        output = ImageOps.fit(member_photo, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output = output.resize((950,950))
        circle_white.paste(output, (38,38), output)
        circle_white = circle_white.resize((256,256))
        
        img = Image.open("resources/background.png").resize((1024,512))
        img.paste(circle_white, (376,25), circle_white)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("resources/font.ttf", 36)
        font_name = ImageFont.truetype("resources/font.ttf", 50)

        text = "Bienvenido"
        if self.insult:
            insulto = ""
            for _ in range(0,100):
                insulto = services.common.get_insulto_aleatorio().lower()
                if insulto.__len__() < 30:
                    break

            text += " %s" % insulto

        border_color = "black"
        text_color = self.embed_color

        draw.text((511,374), text, fill=border_color, font=font, anchor="mm")
        draw.text((513,376), text, fill=border_color, font=font, anchor="mm")
        draw.text((512,375), text, fill=text_color, font=font, anchor="mm")

        draw.text((511,434), member.name, fill=border_color, font=font_name, anchor="mm")
        draw.text((513,436), member.name, fill=border_color, font=font_name, anchor="mm")
        draw.text((512,435), member.name, fill=text_color, font=font_name, anchor="mm")
        img.save("tmp.png")
        await channel.send(file=discord.File("tmp.png", filename="welcome.png"))
        os.remove("tmp.png")

    async def on_member_join(self, member:discord.Member):
        if not self.welcome_members: return
        await self.welcome(member)

while True:
    try:
        bot = felaciano(scripts_file, prefix=prefix, language=language, logger=logger, connect=connect_channels, welcome=welcome_memebrs, insult=insult, join_chance=prob)
        bot.run(api_key)
    except RuntimeError:
        break
    except Exception as e:
        logger.error(e)
        print("%s exception, exiting in %d seconds..." % (e, EXIT_TIME))
        sleep(EXIT_TIME)
        exit()