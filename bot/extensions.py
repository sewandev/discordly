from typing import Any

from discord.ext import commands

from bot.bot import Bot

async def setup(bot: Bot) -> None:
    await bot.load_extension('cogs.core')
    await bot.load_extension('cogs.voice')