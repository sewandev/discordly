import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup  # Importación necesaria

from config.config import Config

class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,
            case_insensitive=True
        )

    async def setup_hook(self) -> None:
        """Configuración inicial del bot"""
        await self.load_extension('bot.extensions')
        await self.sync_application_commands()  # Método propio de Pycord 2.x

    async def sync_application_commands(self) -> None:
        """Sincroniza los comandos de aplicación con Discord"""
        try:
            if Config.GUILD_ID:
                guild = discord.Object(id=Config.GUILD_ID)
                self.application_commands.copy_global_to(guild=guild)
                synced = await self.application_commands.sync(guild=guild)
            else:
                synced = await self.application_commands.sync()
                
            logging.info(f'Comandos de aplicación sincronizados: {len(synced)} comandos')
        except Exception as e:
            logging.error(f'Error sincronizando comandos: {e}')

    async def on_ready(self) -> None:
        """Evento cuando el bot está listo"""
        logging.info(f'Bot conectado como {self.user} (ID: {self.user.id})')
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="/test_welcome"
        ))

    @staticmethod
    def setup_logging() -> None:
        """Configura el sistema de logging"""
        Path('logs').mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                RotatingFileHandler(
                    Config.LOG_FILE,
                    mode='w',
                    maxBytes=5*1024*1024,
                    backupCount=2,
                    encoding='utf-8'
                ),
                logging.StreamHandler()
            ],
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )