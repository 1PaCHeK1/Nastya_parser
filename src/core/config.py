import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseSettings

from bot.core.config import (
    BotSettings,
    DevBotSettings,
    ProdBotSettings
)


base_dir = Path(__file__).absolute().parent.parent


class Settings(BaseSettings):
    app_name: str = "Parser"
    debug: bool

    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_url: str

    redis_host: str
    redis_port: int
    redis_url: str

    bot: BotSettings

    cert_file_path: str


class DevSettings(Settings):
    debug: bool = True

    db_name: str = "parser"
    db_host: str = "localhost"
    db_port: int = 6000
    db_user: str = "root"
    db_pass: str = "root"
    db_url: str = "postgresql://root:root@localhost:6000/parser"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_url: str = "redis://localhost:6379"

    bot: DevBotSettings = DevBotSettings()

    cert_file_path: str = ""


class ProdSettings(Settings):
    debug: bool = False

    bot: ProdBotSettings

    class Config:
        env_nested_delimiter = "."
        env_file = base_dir / ".env", base_dir / ".env.prod"
        env_file_encoding = "utf-8"


def get_config(environment: str|None = None):
    if environment is None:
        load_dotenv(base_dir / ".env")
        environment = os.getenv("environment")

    match environment:
        case "dev":
            return DevSettings()
        case "test":
            return DevSettings()
        case "prod":
            return ProdSettings()
        case _:
            raise ValueError
