from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from .database import Database
from .users import services as user_services


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(
        Database,
        db_url="postgresql://root:root@db:5432/parser"
    )

    user_service = providers.Factory(
        user_services.UserService,
        session=database.provided.session,
    )
