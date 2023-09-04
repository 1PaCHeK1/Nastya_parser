from typing import Never
from bot.engine import create_bot, create_dispatcher
from core.container import create_container
from settings import BotSettings, get_settings
from sentry import init as sentry_init


def polling() -> Never:
    sentry_init()
    container = create_container()
    config = get_settings(BotSettings)

    bot = create_bot(config)
    dp = create_dispatcher(container)

    dp.run_polling(bot)


def webhook() -> Never:
    sentry_init()
    container = create_container()
    config = get_settings(BotSettings)

    bot = create_bot(config)
    dp = create_dispatcher(container)

    dp.run_polling(bot)
