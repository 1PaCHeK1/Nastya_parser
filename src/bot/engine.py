import aioinject
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from bot.middlewares import AIOInjectMiddleware
from bot.routers import (
    image_router,
    other_router,
    quize_router,
    registration_router,
    word_router,
)
from settings import BotSettings


async def on_startup(bot: Bot, dispatcher: Dispatcher):
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Запуск бота"),
            types.BotCommand(command="help", description="Информация"),
            types.BotCommand(command="favorites", description="Избранные"),
            types.BotCommand(command="settings", description="Настройки"),
            types.BotCommand(command="list", description="Случайные слова"),
        ],
    )


async def on_shutdown(dp: Dispatcher):
    await dp.bot.delete_webhook()
    container: aioinject.Container = dp["aioinject_container"]
    await container.aclose()


def create_bot(settings: BotSettings) -> Bot:
    return Bot(token=settings.api_token)


def create_dispatcher(container: aioinject.Container) -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp["aioinject_container"] = container

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.outer_middleware.register(AIOInjectMiddleware(container=container))
    dp.callback_query.outer_middleware.register(
        AIOInjectMiddleware(container=container),
    )

    dp.include_routers(
        registration_router,
        other_router,
        quize_router,
        image_router,
        word_router,
    )

    return dp
