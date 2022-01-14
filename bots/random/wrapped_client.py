import discord
import logging
import os
import sys
from abc import abstractmethod, ABC


class ServiceNotFound(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Wrapped_Client(discord.Client):

    def __init__(self, language : dict, services_path : str, prefix : str="", logger : logging.Logger = None) -> None:
        intent = discord.Intents.all()
        super().__init__(intents=intent)
        self.language = language
        self.prefix = prefix
        self.logger = logger if logger else logging.getLogger('bot_client')
        self.embed_color = int(self.language["EMBED_COLOR_CORRECT"],16)
        self.embed_color_error = int(self.language["EMBED_COLOR_ERROR"],16)
        error_title = self.language["COMMANDS"]["ERROR_TITLE"]
        error_msg = self.language["COMMANDS"]["COMMAND_ERROR"]
        embed=discord.Embed(color=self.embed_color_error)
        embed.add_field(name=error_title, value=error_msg)
        self.embed_error = embed
        self.services = __load_services__(services_path, self.language["COMMANDS"]["AVAILABLE_COMMANDS"])

    def get_service(self, name):
        if not name in self.services:
            raise ServiceNotFound()
        return self.services[name]

    async def execute_service(self, service_name, **options):
        try:
            code, _ = self.get_service(service_name.lower())
            await code(**options)
        except ServiceNotFound:
            pass
        except:
            message=options["message"]
            await message.channel.send(embed=self.embed_error)

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
