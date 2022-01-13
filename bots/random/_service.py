import os
import sys
from abc import abstractmethod, ABC


services = {}

class ServiceNotFound(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class service(ABC):

    def __init__(self, name : str, aliases : list, description : str) -> None:
        self.name = name
        self.aliases = aliases
        self.description = description

    async def __execute__(self, *args, **kwards):
        await self.__run__(*args, **kwards)

    @abstractmethod
    async def __run__(self, *args, **kwards):
        return

def load_services(services_path, commands_description):
    services_path = os.path.abspath(services_path)
    services_on_dir = __get_scripts__(services_path)
    sys.path.append(services_path)
    for service_name in services_on_dir:
        try:
            command_info = commands_description[service_name.upper()]
            aliases = command_info["ALIASES"]
            description = command_info["DESCRIPTION"]
            loaded_module = __get_valid_service__(service_name)
            new_service = __initialize_module__(loaded_module, service_name, aliases, description)
            code = new_service.__run__
            aliases.append(service_name)
            for alias in aliases:
                services[alias.lower()] = (code, new_service)
        except (ModuleNotFoundError, AttributeError, TypeError, KeyError):
            pass
    sys.path.remove(services_path)

def __initialize_module__(loaded_module, *args, **kwards):
    new_service = loaded_module(*args, **kwards)
    return new_service

def __get_valid_service__(service_name):
    module = __import__(service_name)
    run = getattr(module, "__run__")
    loaded_module = type(service_name, (service,), {"__run__":run})
    return loaded_module

def __get_scripts__(scripts_path):
    scripts_on_dir = os.listdir(scripts_path)
    services_on_dir = [f[:-3] for f in scripts_on_dir if (os.path.isfile(os.path.join(scripts_path, f)) and not f[0] == '_')]
    return services_on_dir

def get_service(name):
    if not name in services:
        raise ServiceNotFound()
    return services[name]
