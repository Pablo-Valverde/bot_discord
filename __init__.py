#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from PIL import Image,ImageFont,ImageDraw,ImageOps
from dotenv import load_dotenv 
import io
import json
import argparse
import random
import sys
import services.common
import pydiscord
import os
import logging
import discord
import traceback


load_dotenv(dotenv_path=".environ.env")

EXIT_TIME = 10

#def __parse__():
#    parser = argparse.ArgumentParser()
#    parser.add_argument(
#        '-CONFIG_FILE',
#        '-conf',
#        type=lambda s: str(s),
#        default='config/config.json',
#        help='Configuration file'
#    )
#    parser.add_argument(
#        '-SCRIPTS_DIR',
#        '-scripts',
#        type=lambda s: str(s),
#        default='services',
#        help='Scripts directory'
#    )
#    parser.add_argument(
#        '-LANGUAGUE_FILE',
#        '-lang_file',
#        type=lambda s: str(s),
#        default='languages/docs.json',
#        help='Languages file'
#    )
#    languages = json.load(open(parser.parse_args().LANGUAGUE_FILE))
#    available_languages = [language for language in languages]
#    parser.add_argument(
#        '-LANGUAGE',
#        '-bot_lang',
#        type=lambda s: str(s),
#        default=available_languages[0], 
#        choices=available_languages
#    )
#    return parser.parse_args()
#
#script_dir = os.path.dirname(__file__)
#args = __parse__()
#
#init_time = datetime.datetime.now()
#config = json.load(open(args.CONFIG_FILE))
#language = json.load(open(args.LANGUAGUE_FILE))[args.LANGUAGE]
#
#log_directory = config['LOG_DIRECTORY']
#log_extension = config['LOG_FILE_EXT'].replace('.', '')
#prefix = config['PREFIX']
#
#root = logging.getroot('discord')
#root.setLevel(logging.INFO)
#log_file = '%s/%s.%s' % (log_directory, init_time.strftime('%Y-%m-%d_%H-%M'), log_extension)
#if not os.path.isdir(log_directory):
#    if not os.path.exists(log_directory):
#        root.info("Created directory '%s'" % log_directory)
#        os.mkdir(log_directory)
#    else:
#        root.error("'%s' is a file, not a directory for the logs." % log_directory)
#        print("'%s' is a file, not a directory for the logs. exiting in %d seconds..." % (log_directory,EXIT_TIME))
#        sleep(EXIT_TIME)
#        exit()
#
#handler = logging.FileHandler(filename="%s/%s" % (script_dir,log_file), encoding='utf-8', mode='w+')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#root.addHandler(handler)
#
#api_key = config['BOT_KEY']
#scripts_path = args.SCRIPTS_DIR
#if not os.path.isdir(scripts_path):
#    root.error("'%s' is not a directory. Check if it exists." % scripts_path)
#    print("'%s' is not a valid scripts directory. exiting in %d seconds..." % (scripts_path,EXIT_TIME))
#    sleep(EXIT_TIME)
#    exit()
#
#welcome_memebrs = config['ON_MEMBER_JOIN']['ENABLED']
#insult = config['ON_MEMBER_JOIN']['INSULT']
#
#connect_channels = config['ON_VOICE_STATE_UPDATE']['ENABLED']
#prob = config['ON_VOICE_STATE_UPDATE']['CHANCE']

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-services",
        "-s",
        type=lambda s: str(s),
        default="services",
        help="Services path"
    )
    parser.add_argument(
        "-language",
        "-lang",
        "-l",
        type=lambda s: json.load(open(s)),
        default=None,
        help="JSON file with the information of the services and the bot"
    )
    parser.add_argument(
        "-configuration",
        "-conf",
        "-c",
        type=lambda s: json.load(open(s)),
        default=None,
        help="Configuration file for felaciano"
    )
    parser.add_argument(
        "-prefix",
        "-p",
        type=lambda s: str(s),
        default="-",
        help="Prefix of the bot"
    )
    parser.add_argument(
        "-api_key",
        "-key",
        type=lambda s: str(s),
        default=os.getenv("API_KEY"),
        help="Bot key"
    )

    return parser.parse_args()

args = parse()

root = logging.getLogger("felaciano")
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

scripts_path = args.services
prefix = args.prefix
language = args.language
api_key = args.api_key

if not api_key:
    root.error("No API_KEY has been given, add one on '.environ.env' or use the argument -api_key.")
    exit()

conf = args.configuration
connect_channels = True
prob = 0.01
welcome_members = True
insult = True
if conf:
    conf:dict
    on_voice_state_update = conf.get("ON_VOICE_STATE_UPDATE")
    on_member_join = conf.get("ON_MEMBER_JOIN")
    if on_voice_state_update:
        aux_connect_channels = on_voice_state_update.get("ENABLED")
        connect_channels = aux_connect_channels if aux_connect_channels else connect_channels
        aux_prob = on_voice_state_update.get("CHANCE")
        prob = aux_prob if aux_prob else prob
    if on_member_join:
        aux_welcome_members = on_member_join.get("ENABLED")
        welcome_members = aux_welcome_members if aux_welcome_members else welcome_members
        aux_insult = on_member_join.get("INSULT")
        insult = aux_insult if aux_insult else insult

class felaciano(pydiscord.Wrapped_Client):

    def __init__(self, services_path: str, prefix: str = "", language: dict = None, connect = True, welcome = True, insult = True, join_chance = 0.02) -> None:
        super().__init__(services_path, prefix=prefix, language=language)
        if not os.path.isdir("resources"):
            if not os.path.exists("resources"):
                root.info("Created directory 'resources'")
                os.mkdir("resources")
            else:
                root.warning("'resources' should be a directory")
        if os.path.isdir("resources"):
            if not os.path.isdir("resources/respiraciones/"):
                if not os.path.exists("resources/respiraciones/"):
                    root.info("Created directory 'resources/respiraciones/'")
                    os.mkdir("resources/respiraciones/")
                else:
                    root.warning("'resources/respiraciones/' should be a directory")
        self.connect_channels = connect
        self.prob = join_chance
        self.welcome_members = welcome
        self.insult = insult

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="el porn-channel")
        await self.change_presence(activity=activity)
        root.info('Bot started correctly')
    
    async def on_message(self, message:discord.Message):
        if message.author.bot: return
        permissions = message.channel.permissions_for(message.guild.me)
        if not (permissions.send_messages and permissions.embed_links): return
        if not self.is_ready():
            await message.channel.send("Pero subnormal, dejame llegar al ordenador al menos.")
            return
        await super().on_message(message)

    async def on_error(self, event_method, *args, **kwargs):
        e = sys.exc_info()[1]
        buffer = ""
        for a in traceback.format_tb(sys.exc_info()[2]):
            buffer += a
        root.error("\n%s%s" % (buffer, e))
        print("%s%s\nNon-fatal exception" %  (buffer, e))

    async def on_voice_state_update(self, member, before, after):
        if not self.connect_channels: return
        if member.bot: return
        if not self.is_ready(): return
        if not after.channel: return
        if after.channel == before.channel: return
        channel = after.channel
        if not channel: return
        permissions = channel.permissions_for(channel.guild.me)
        if not (permissions.connect and permissions.speak): return
        roll = random.random()*100
        if roll <= float(self.prob * 100):
            self.sound_channel = discord.utils.get(self.voice_clients, guild = channel.guild)
            if self.sound_channel:  await self.sound_channel.move_to(channel)
            else:                   self.sound_channel = await channel.connect()
            root.info("Connected to channel with ID %d, got roll %.3f <= %.3f" % (channel.id, roll, float(self.prob * 100)))
            if self.sound_channel.is_playing(): return
            if not os.path.isdir("resources/respiraciones/"):
                root.warning("'resources/respiraciones/' is missing, create it or the bot will only join silently...")
                return
            scripts_on_dir = os.listdir("resources/respiraciones/")
            sounds_on_dir = [f for f in scripts_on_dir if (os.path.isfile(os.path.join("resources/respiraciones/", f)) and f.find(".mp3") > -1)]
            if sounds_on_dir.__len__() == 0:
                root.warning("'resources/respiraciones/' got no .mp3 files, add some so the bot can play sound, joinning silently...")
                return
            sound = random.choice(sounds_on_dir)
            root.info("Selected soundtrack '%s'" % sound)
            self.sound_channel.play(discord.FFmpegPCMAudio("resources/respiraciones/%s" % sound))

    async def welcome(self, member):
        channel = member.guild.system_channel
        permissions = channel.permissions_for(channel.guild.me)
        if not (permissions.send_messages and permissions.attach_files): return
        if not channel:
            root.info("Can't welcome user ID %d. No channel selected in guild ID %d" % (member.id, member.guild.id))
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
        await channel.send(member.mention, file=discord.File("tmp.png", filename="welcome.png"))
        os.remove("tmp.png")
        root.info("User ID %d correctly welcomed" % member.id)

    async def on_member_join(self, member:discord.Member):
        if not self.welcome_members: return
        root.info("Trying to welcome user with ID %d" % member.id)
        await self.welcome(member)

while True:
    try:
        bot = felaciano(scripts_path, prefix=prefix, language=language, connect=connect_channels, welcome=welcome_members, insult=insult, join_chance=prob)
        bot.run(api_key)
    except RuntimeError:
        break
    except Exception as e:
        buffer = ""
        for a in traceback.format_tb(sys.exc_info()[2]):
            buffer += a
        root.error("\n%s" % buffer)
        print("%sfatal exception, exiting in %d seconds..." % (e, EXIT_TIME))
        sleep(EXIT_TIME)
        break
