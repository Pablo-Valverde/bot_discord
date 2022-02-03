import json
import discord
import logging
import os
import sys
from abc import abstractmethod, ABC


LANG_FILE = "docs.json"
DEFAULT_LANGUAGE = {
    "COMMANDS":{
        "AVAILABLE_COMMANDS":{
            "PING":{
                "ALIASES":[
                    "LATENCIA"
                ],
                "DESCRIPTION": "Muestra la latencia del bot"
            },
            "HELP":{
                "ALIASES":[
                    "COMANDOS",
                    "CMDS"
                ],
                "DESCRIPTION": "Muestra el menu de ayuda"
            },
        },
        "ALIAS":"Alias",
        "ERROR_TITLE":"Error",
        "COMMAND_ERROR":"Ha ocurrido un error inesperado al ejecutar el comando",
        "NO_USERS":"No hay usuarios"
    },
    "EMBED_COLOR":"0xffd79e",
    "EMBED_COLOR_ERROR":"0xffa3a3"
}

root = logging.getLogger("bot-discord")
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

class ServiceNotFound(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class dict_decorator(dict):

    def update(self, __m):
        for key in __m:
            m_value = __m[key]
            if not self.get(key):
                self[key] = m_value
                continue
            self_value = self[key]
            if type(m_value) == dict:
                if type(self_value) == dict:
                    _ = dict_decorator(self_value)
                    _.update(m_value)
                    self[key] = _
                else:
                    self[key] = m_value

class Wrapped_Client(discord.Client):

    def __init__(self, services_path : str, prefix : str="", language : dict = None) -> None:
        if not language:
            language = DEFAULT_LANGUAGE
            if not os.path.exists(LANG_FILE):
                fp = open(LANG_FILE, "w")
                json.dump(DEFAULT_LANGUAGE, fp, indent=4)
                fp.close()
        else:
            language = dict_decorator(language)
            language.update(DEFAULT_LANGUAGE)
        intent = discord.Intents.all()
        super().__init__(intents=intent)
        self.language = language
        self.prefix = prefix

        self.embed_color = int(self.language["EMBED_COLOR"],16)
        self.embed_color_error = int(self.language["EMBED_COLOR_ERROR"],16)
        self.no_users = self.language["COMMANDS"]["NO_USERS"]
        error_title = self.language["COMMANDS"]["ERROR_TITLE"]
        error_msg = self.language["COMMANDS"]["COMMAND_ERROR"]
        self.services = __load_services__(services_path, self.language["COMMANDS"]["AVAILABLE_COMMANDS"])

        embed=discord.Embed(color=self.embed_color_error)
        embed.add_field(name=error_title, value=error_msg)
        self.embed_error = embed

    def get_service(self, name):
        if not name in self.services:
            raise ServiceNotFound()
        return self.services[name]
    
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

    async def on_message(self, message:discord.Message):
        if not message.content: return
        parsed_message = self.parse_message(message)
        if not parsed_message: return
        command, argument = parsed_message
        root.info('"%s" by %d on channel %d of guild %d.' % (message.content, message.author.id, message.channel.id, message.guild.id))
        await self.execute_service(command, message=message, client=self, arguments=argument)

    async def execute_service(self, service_name, **options):
        try:
            code, _ = self.get_service(service_name.lower())
            await code(**options)
        except ServiceNotFound:
            pass

class __service__(ABC):

    def __init__(self, name : str, aliases : list, description : str) -> None:
        self.name = name
        self.aliases = [self.name] + [alias.lower() for alias in aliases]
        self.description = description

    @abstractmethod
    async def __run__(self, *args, **kwards):
        return

def __load_services__(services_path, commands_description):
    services = {}
    default_path = os.path.abspath(os.path.dirname(__file__) + "/default_services")
    default_services = __get_scripts__(default_path)
    services_path = os.path.abspath(services_path)
    available_services = __get_scripts__(services_path)
    sys.path += [services_path, default_path]
    for service_name in default_services + available_services:
        services.update(__load_service__(commands_description, service_name))
    sys.path = sys.path[:-2]
    return services

def __load_service__(commands_description, service_name):
    services = {}
    try:
        loaded_module = __get_valid_service__(service_name)
        new_service = __get_service_info__(service_name, commands_description, loaded_module)
        code = new_service.__run__
        for alias in new_service.aliases:
            services[alias.lower()] = (code, new_service)
    except (ModuleNotFoundError, AttributeError, TypeError, KeyError):
        pass
    return services

def __get_service_info__(service_name, commands_description, object):
    command_info = commands_description[service_name.upper()]
    aliases = command_info["ALIASES"]
    description = command_info["DESCRIPTION"]
    return __initialize_module__(object, service_name, aliases, description)

def __get_scripts__(scripts_path):
    scripts_on_dir = os.listdir(scripts_path)
    services_on_dir = [f[:-3] for f in scripts_on_dir if (os.path.isfile(os.path.join(scripts_path, f)) and not f[0] == '_')]
    return services_on_dir

def __get_valid_service__(service_name):
    module = __import__(service_name)
    run = getattr(module, "__run__")
    loaded_module = type(service_name, (__service__,), {"__run__":run})
    return loaded_module

def __initialize_module__(loaded_module, *args, **kwards):
    new_service = loaded_module(*args, **kwards)
    return new_service
