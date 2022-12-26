from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from parsers.container import ParserContainer

from .config import DevSettings
from .database import Database
from .users import services as user_services
from .utils import services as util_services


class Container(containers.DeclarativeContainer):
    
    config = providers.Resource(DevSettings)
    
    database = providers.Singleton(
        Database,
        db_url=config.provided.database_connection_url
    )

    redis_service = providers.Factory(
        util_services.RedisService,
        redis_url=config.provided.redis_connection_url
    )

    user_service = providers.Factory(
        user_services.UserService,
        session=database.provided.session,
    )

    _parser = providers.Container(
        ParserContainer
    )

    # word_service = providers.Factory(
    #     ...,
    #     session=database.provided.session,
    #     parser=_parser
    # )
