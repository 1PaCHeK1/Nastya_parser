from fastapi import FastAPI
from settings import get_settings, FastApiSettings
from starlette.middleware.cors import CORSMiddleware
from sentry import init as sentry_init
from core.containers import Container
from api.router import word_router


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

    app.add_middleware(
        CORSMiddleware,
        allow_methods=["*"],
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