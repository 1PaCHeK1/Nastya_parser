from business_validator import ValidationError
from fastapi import FastAPI
from settings import get_settings, FastApiSettings
from starlette.middleware.cors import CORSMiddleware
from aioinject.ext.fastapi import InjectMiddleware
from sentry import init as sentry_init
from core.container import create_container
from api.router import router
from api.handlers import handle_validation_errors


def create_fastapi() -> FastAPI:
    sentry_init()

    api_settings = get_settings(FastApiSettings)

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
