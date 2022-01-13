from . import _service
import discord
import logging



class Wrapped_Client(discord.Client):

    def __init__(self, language : dict, services_path : str, prefix : str="", logger : logging.Logger=logging.getLogger('bot_client')) -> None:
        insultos = "negro hijo de la gran puta-forro de mierda-transexual seudosimio de mierda-putofobico del orto mal-parido aborto fallido de la naturaleza-culo roto pijeado-chupa pijas succiona Soretes-choclofobico-dildo culeado inmeurable mar de pajero-vaca gorda lechera-teton pelotudo-dinosaurio traga hormigas-elefante travesti gay traga culos-gordo sordo atragantado con porongas-Ojalá te viole un negro camionero nazi-hijo de la gran re putisima madre que te lo re mil pario-seudopajero etereo sorete radioactivo-tirate de un puente obeso volador huele pedos balanzafobico panzon-come truchas-conchudo atragantado-ciego escupe mierda-pene retráctil-viejo conchudo-tarado inútil sempiterno-culo de petricor-cuando hablabas escupis mierda-dislexico traga leche-gorda vaca-conspicuofobico superfluo de mierda-no servis hilo de down mogolico que sos autista-la Concha de tu vieja puta-enfermo de mierda violador de cangrejos-porongeado del orto dilucidio de inservible-ojala te viole darthes-vilipendio a la humanidad suicidate-enfermito tarado-zorro putita barata-coje viejas macrista con parkingson-bin diesel con cáncer-te pareces a carlitos-con esa cara de pelotudo bruto villero-volvé a la escuela inestrictado tubular de culos-escucha porno necrofilico-pendejo egipcio-retrasado vikingo mira pitos-coje arboles-viola perros-toma termidor chetofobico-pobre de mierda volvé a tu casa de cartón radioactiva-camión lleno de negros que te trajeron en un container de chernobyl-tontito huele pedos-balanzafobico panzon come truchas-conchudo atragantado-ciego escupe mierda proxoneta-garcha consolas virgen-mongolo azteca no la pones ni con un palo-drogadicto-asesino cancerigenico pajero hecho de plutonio-autista de mierda-eres un quintana-payaso de mierda-te huelen los pies igual que al parse-gordo forro-gorio-chupavergas-andá al porn channel a cascartela-piltrafilla-eres un cabestro-eres mas pedofilo que energuia-lerdo come longanizas-lamesables-muerdealmohadas-alcubillano de mierda-toca tubas-costalero-nazareno-clown-me quedé sin insultos que decirte, esa cara de mierda me dejó sin palabras-"
        self.insultos = insultos.split("-")
        
        intent = discord.Intents.default()
        intent.messages = True
        intent.members = True
        super().__init__(intent=intent)
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
        await self.change_name()
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

    async def change_name(self):
        import time
        guild = await self.fetch_guild(843443913557934080)
        nombres = ["🙉🍌ⒶⓊⓉⒾⓈⓉ🤡🎈", "🎈🙉ⒶⓊⓉⒾⓈⓉ🍌🤡", "🤡🎈ⒶⓊⓉⒾⓈⓉ🙉🍌", "🍌🤡ⒶⓊⓉⒾⓈⓉ🎈🙉", "🙉🍌ⒶⓊⓉⒾⓈⓉ🤡🎈"]
        while True:
            nombre = nombres.pop(0)
            nombres.append(nombre)
            await guild.edit(name=nombre)
            time.sleep(1)
