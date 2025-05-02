from bot.bot import Bot
from config.config import Config

def main() -> None:
    Bot.setup_logging()
    bot = Bot()
    bot.run(Config.DISCORD_TOKEN)

if __name__ == '__main__':
    main()