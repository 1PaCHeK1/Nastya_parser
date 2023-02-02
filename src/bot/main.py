import argparse
from aiogram import executor, Dispatcher, types
from aiogram.utils.executor import start_webhook

from core.containers import Container
from core.config import get_config
from bot.commands import dp


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


async def on_startup(dp:Dispatcher):
    config, args = dp["config"], dp["args"]
    if args.mode == "webhook":
        with open(config.cert_file_path, "rb") as cert_file:
            await dp.bot.set_webhook(
                config.bot.webhook_host + config.bot.webhook_path,
                certificate=cert_file,
            )
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запуск бота"),
        types.BotCommand("help", "Информация"),
        types.BotCommand("favorites", "Избранные"),
        types.BotCommand("settings", "Настройки"),
        types.BotCommand("list", "Случайные слова"),
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
    args = arg_parse()
    config = get_config()

    dp["config"] = config
    dp["args"] = args

    if args.mode == "polling":
        executor.start_polling(
            dp,
            on_startup=on_startup,
            on_shutdown=
        )
    else:
        start_webhook(
            dp,
            webhook_path=config.bot.webhook_path,
            on_startup=on_startup,
            host=config.bot.webapp_host,
            port=config.bot.webapp_port,
        )


if __name__ == "__main__":
    main()
