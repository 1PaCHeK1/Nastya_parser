import argparse
import sentry_sdk
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
        webhook = await dp.bot.get_webhook_info()
        if webhook.url != config.bot.webhook_path:
            await dp.bot.delete_webhook()
        await dp.bot.set_webhook(
            "https://" + config.bot.webhook_host + config.bot.webhook_path,
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
    sentry_sdk.init(
        dsn="https://7a7685a757924dc7ad2d539e2a2aec78@o4504611526672384.ingest.sentry.io/4504611528638464",
        traces_sample_rate=1.0
    )

    args = arg_parse()
    config = get_config()

    dp["config"] = config
    dp["args"] = args

    if args.mode == "polling":
        executor.start_polling(
            dp,
            on_startup=on_startup,
        )
    else:
        start_webhook(
            dispatcher=dp,
            webhook_path=config.bot.webhook_path,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=config.bot.webapp_host,
            port=config.bot.webapp_port,
        )


if __name__ == "__main__":
    main()
