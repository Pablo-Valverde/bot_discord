#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
from PIL import Image,ImageFont,ImageDraw,ImageOps
import json
import argparse
import random
import services.common
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

welcome_memebrs = config['WELCOME']
connect_channels = config['CONNECT']

class felaciano(pydiscord.Wrapped_Client):

    def __init__(self, language: dict, services_path: str, prefix: str = "", logger: logging.Logger = None, connect = True, welcome = True) -> None:
        super().__init__(language, services_path, prefix, logger)
        self.sound_channel = None
        self.connect_channels = connect
        self.welcome_members = welcome

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="el porn-channel")
        await self.change_presence(activity=activity)
        self.logger.info('Bot is ready.')
    
    async def on_message(self, message:discord.Message):
        if message.author.bot: return
        if not self.is_ready():
            await message.channel.send("Pero subnormal, dejame llegar al ordenador al menos.")
            return
        await super().on_message(message)

    async def on_voice_state_update(self, member, before, after):
        if not self.connect_channels: return
        if member.bot: return
        if not after.channel: return
        channel = after.channel
        if not channel: return
        roll = random.randint(0,100)
        if roll <= 100:
            if self.voice_clients:
                await self.voice_clients[0].disconnect()
            await channel.connect()
            self.sound_channel = discord.utils.get(self.voice_clients, guild = channel.guild)
            scripts_on_dir = os.listdir("resources/respiraciones/")
            sounds_on_dir = [f for f in scripts_on_dir if (os.path.isfile(os.path.join("resources/respiraciones/", f)) and f.find(".mp3") > -1)]
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
        font = ImageFont.truetype("ariblk.ttf", 36)
        font_name = ImageFont.truetype("ariblk.ttf", 50)

        insulto = ""
        for _ in range(0,100):
            insulto = services.common.get_insulto_aleatorio().lower()
            if insulto.__len__() < 30:
                break

        text = "Bienvenido %s" % insulto

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
        bot = felaciano(language, scripts_file, prefix=prefix, logger=logger, connect=connect_channels, welcome=welcome_memebrs)
        bot.run(api_key)
    except RuntimeError:
        break
    except Exception as e:
        logger.error(e)