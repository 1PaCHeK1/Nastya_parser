from fastapi import FastAPI
from sentry import init as sentry_init


def create_fastapi() -> FastAPI:
    sentry_init()
