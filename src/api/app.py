from aioinject.ext.fastapi import InjectMiddleware
from business_validator import ValidationError
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.handlers import handle_validation_errors
from api.router import router
from core.container import create_container
from sentry import init as sentry_init
from settings import FastApiSettings, get_settings


def create_fastapi() -> FastAPI:
    sentry_init()

    get_settings(FastApiSettings)

    app = FastAPI()
    app.container = create_container()

    app.add_middleware(
        CORSMiddleware,
        allow_methods=["*"],
    )
    app.add_middleware(InjectMiddleware, container=app.container)
    app.add_exception_handler(
        ValidationError,
        handle_validation_errors,
    )

    @app.get("/healthcheck/")
    async def healthcheck() -> None:
        return None

    app.include_router(router)

    return app
