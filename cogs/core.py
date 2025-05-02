import logging
from typing import Any

import discord
from discord.ext import commands
from discord.commands import slash_command  # Decorador correcto

from bot.bot import Bot
from config.config import Config

class Core(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @slash_command(
        name="test_welcome",
        description="Simula el mensaje de bienvenida",
        guild_ids=[Config.GUILD_ID] if Config.GUILD_ID else None
    )
    async def test_welcome(self, ctx: discord.ApplicationContext) -> None:
        """Manejador del comando slash"""
        logging.info(f'Testing welcome message by {ctx.author.display_name}')
        await ctx.respond(
            f'¡Bienvenido {ctx.author.mention}! (Mensaje de prueba)',
            ephemeral=True
        )

async def setup(bot: Bot) -> None:
    await bot.add_cog(Core(bot))