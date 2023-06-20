from aioinject import Container, Callable, Singleton, Object
from sqlalchemy.orm import Session

from settings import (
    DatabaseSettings,
    RedisSettings,
    AppSettings,
    FastApiSettings,
    SentrySettings,
    BotSettings,
    get_settings,
)

from db.base import Database, get_session
from .users import services as user_services
from .words import services as word_services
from .caches import services as cache_services
from .image import services as image_services


def create_container() -> Container:
    container = Container()

    for settings_type in [
        DatabaseSettings,
        RedisSettings,
        AppSettings,
        FastApiSettings,
        SentrySettings,
        BotSettings,
    ]:
        container.register(Object(get_settings(settings_type), settings_type))

    container.register(Singleton(Database))
    container.register(Callable(get_session, Session))

    container.register(Callable(user_services.UserService))

    container.register(Callable(word_services.WordService))
    container.register(Callable(word_services.TranslateWordService))

    container.register(Callable(cache_services.RedisService))

    container.register(Callable(image_services.ImageProcessService))

    return container
