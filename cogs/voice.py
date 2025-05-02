import logging
from typing import Any

import discord
from discord.ext import commands, tasks

from bot.bot import Bot

class Voice(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.check_empty_voice.start()

    def cog_unload(self) -> None:
        self.check_empty_voice.cancel()

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState
    ) -> None:
        if member.bot:
            return

        voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
        if voice_client and len(voice_client.channel.members) == 1:
            await voice_client.disconnect()
            logging.info(f'Disconnected from empty voice channel in {member.guild.name}')

    @tasks.loop(seconds=10)
    async def check_empty_voice(self) -> None:
        for voice_client in self.bot.voice_clients:
            if len(voice_client.channel.members) == 1:
                await voice_client.disconnect()
                logging.info(f'Disconnected from empty voice channel in {voice_client.guild.name}')

    @check_empty_voice.before_loop
    async def before_check_empty_voice(self) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: Bot) -> None:
    await bot.add_cog(Voice(bot))