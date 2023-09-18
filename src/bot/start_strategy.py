import asyncio
from typing import Never

from bot.engine import create_bot, create_dispatcher
from core.container import create_container
from sentry import init as sentry_init
from settings import BotSettings, get_settings


def polling() -> Never:
    sentry_init()
    container = create_container()
    config = get_settings(BotSettings)

    bot = create_bot(config)
    dp = create_dispatcher(container)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(dp.start_polling(bot))


def webhook() -> Never:
    sentry_init()
    container = create_container()
    config = get_settings(BotSettings)

    bot = create_bot(config)
    dp = create_dispatcher(container)

    dp.run_polling(bot)
