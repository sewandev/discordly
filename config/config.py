import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
    LOG_FILE = Path('logs/bot.log')