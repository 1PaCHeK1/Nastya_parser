from business_validator import ErrorSchema, ValidationError
from fastapi import FastAPI
from settings import get_settings, FastApiSettings
from starlette.middleware.cors import CORSMiddleware
from aioinject.ext.fastapi import InjectMiddleware
from sentry import init as sentry_init
from core.containers import Container
from core.depends import create_container
from api.router import word_router
from api.handlers import handle_validation_errors


def create_fastapi() -> FastAPI:
    sentry_init()

    container = Container()
    container.init_resources()
    container.wire(packages=[
        "api.depends",
        "api.router.word",
    ])

    api_settings = get_settings(FastApiSettings)

    app = FastAPI()
    app.container = container
    app.aicontainer = create_container()

    app.add_middleware(
        CORSMiddleware,
        allow_methods=["*"],
    )
    app.add_middleware(InjectMiddleware, container=app.aicontainer)
    app.add_exception_handler(
        ValidationError,
        handle_validation_errors,
    )

    @app.get("/healthcheck/")
    async def healthcheck() -> None:
        return None

    app.include_router(word_router)

    return app


# Запрос:
# Клиент
# -> app
# -> AuthMiddleware
# -> handler (функция обработчик)
# -> AuthMiddleware
# -> Клиент