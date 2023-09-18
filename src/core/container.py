import aio_pika
import aiogram
from aioinject import Callable, Container, Object, Singleton
from sqlalchemy.orm import Session
from taskiq import AsyncBroker
from bot.engine import create_bot

from core.image.usecases import ReadTextFromImageUseCase
from core.posts.query import GetUnreadedPostQuery
from core.posts.repository import PostRepository
from db.base import Database, get_session
from rabbit.channel import create_channel
from rabbit.connection import create_connection
from broker.engine import create_broker
from settings import (
    AppSettings,
    BotSettings,
    DatabaseSettings,
    FastApiSettings,
    RabbitSettings,
    RedisSettings,
    SentrySettings,
    get_settings,
)

from .caches import services as cache_services
from .image import services as image_services
from .mail import services as mail_services
from .users import services as user_services
from .users import usecases as user_cases
from .words import services as word_services


def create_container() -> Container:
    container = Container()

    for settings_type in [
        DatabaseSettings,
        RedisSettings,
        AppSettings,
        FastApiSettings,
        SentrySettings,
        BotSettings,
        RabbitSettings,
    ]:
        container.register(Object(get_settings(settings_type), settings_type))

    container.register(Object(create_broker, AsyncBroker))
    container.register(Singleton(create_bot, aiogram.Bot))
    container.register(Singleton(Database))
    container.register(Singleton(create_connection, aio_pika.abc.AbstractConnection))
    container.register(Callable(create_channel, aio_pika.abc.AbstractChannel))
    container.register(Callable(get_session, Session))
    container.register(Callable(cache_services.RedisService))

    container.register(Callable(mail_services.MailService))
    container.register(Callable(user_services.UserTgService))
    container.register(Callable(user_services.UserService))
    container.register(Callable(user_services.HashService))
    container.register(Callable(user_cases.RegistrationFromApiUseCase))

    container.register(Callable(word_services.WordService))
    container.register(Callable(word_services.TranslateWordService))
    container.register(Callable(word_services.QuizeService))

    container.register(Callable(image_services.ImageProcessService))
    container.register(Callable(ReadTextFromImageUseCase))
    container.register(Callable(GetUnreadedPostQuery))
    container.register(Callable(PostRepository))

    return container
