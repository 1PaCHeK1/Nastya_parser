from dependency_injector import containers, providers

from parsers.container import ParserContainer

from .config import get_config
from .database import Database
from .users import services as user_services
from .words import services as word_services
from .caches import services as cache_services
from .image import services as image_services

class Container(containers.DeclarativeContainer):

    config = providers.Configuration(pydantic_settings=[get_config()])

    database = providers.Singleton(
        Database,
        db_url=config.db_url
    )

    redis_service = providers.Factory(
        cache_services.RedisService,
        redis_url=config.redis_url
    )

    user_service = providers.Factory(
        user_services.UserService,
    )

    _parser = providers.Container(
        ParserContainer
    )
    image_process = providers.Factory(
        image_services.ImageProcessService,
    )
    word_service = providers.Factory(
        word_services.WordService,
        parser_service=_parser.translate_service,
        cache_service=redis_service,
    )
    quize_service = providers.Factory(
        word_services.QuizeService,
    )
