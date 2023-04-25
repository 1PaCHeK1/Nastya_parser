import argparse
import sentry_sdk
from aiogram import Dispatcher, types, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from core.containers import Container
from core.config import get_config

from bot.commands import (
    registration_router,
    other_router,
    quize_router,
    word_router,
)


def arg_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=[
            "polling",
            "webhook"
        ],
        default="polling",
    )

    return parser.parse_args()


async def on_startup(bot: Bot, dispatcher: Dispatcher):
    print(bot, dispatcher)
    config, args = dispatcher["config"], dispatcher["args"]

    await bot.set_my_commands([
        types.BotCommand(command="start", description="Запуск бота"),
        types.BotCommand(command="help", description="Информация"),
        types.BotCommand(command="favorites", description="Избранные"),
        types.BotCommand(command="settings", description="Настройки"),
        types.BotCommand(command="list", description="Случайные слова"),
    ])

    container = Container()
    container.init_resources()
    container.wire(packages=[
        "bot.commands",
        "bot.utils",
    ])


async def on_shutdown(dp:Dispatcher):
    await dp.bot.delete_webhook()


def main():
    sentry_sdk.init(
        dsn="https://7a7685a757924dc7ad2d539e2a2aec78@o4504611526672384.ingest.sentry.io/4504611528638464",
        traces_sample_rate=1.0
    )
    config = get_config()

    bot = Bot(token=config.bot.api_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        registration_router,
        other_router,
        quize_router,
        word_router,
    )
    args = arg_parse()
    config = get_config()

    dp["config"] = config
    dp["args"] = args

    if args.mode == "polling":
        dp.startup.register(on_startup)
        dp.run_polling(bot)
    else:
        exit()
        # start_webhook(
        #     dispatcher=dp,
        #     webhook_path=config.bot.webhook_path,
        #     on_startup=on_startup,
        #     on_shutdown=on_shutdown,
        #     skip_updates=True,
        #     host=config.bot.webapp_host,
        #     port=config.bot.webapp_port,
        # )


if __name__ == "__main__":
    main()
