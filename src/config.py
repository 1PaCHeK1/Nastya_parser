from typing import Literal, TypeVar
from pydantic import BaseSettings, BaseConfig
from functools import lru_cache


TSettings = TypeVar("TSettings", bound=BaseSettings)



def get_config(settings: type[TSettings]) -> TSettings:
    return settings()


class SentrySettings(BaseSettings):
    dsn: str | None = None
    traces_sample_rate: float = 1.0

    class Config(BaseConfig):
        env_prefix = "sentry_"


class DatabaseSettings(BaseSettings):
    name: str = "localhost"
    host: str
    port: int = 5432
    user: str
    password: str
    url: str

    echo: bool = True

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config(BaseConfig):
        env_prefix = "db_"


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    url: str

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"

    class Config(BaseConfig):
        env_prefix = "redis_"


class AppSettings(BaseSettings):
    name: str = "Parser"
    debug: bool = True
    environment: Literal["local"] | Literal["dev"] | Literal["prod"]
    cert_file_path: str = ""

    class Config(BaseConfig):
        env_prefix = "app_"


class BotSettings(BaseSettings):
    api_token: str

    webhook_host: str
    webhook_path: str
    webapp_host: str
    webapp_port: int

    class Config(BaseConfig):
        env_prefix = "bot_"


class FastApiSettings(BaseSettings):
    class Config(BaseConfig):
        env_prefix = "api_"


class ContainterSettings:
    sentry: SentrySettings
    app: AppSettings
    bot: BotSettings
    api: FastApiSettings
    database: DatabaseSettings
    redis: RedisSettings

    def __init__(self) -> None:
        self.sentry = get_config(SentrySettings)
        self.app = get_config(AppSettings)
        self.bot = get_config(BotSettings)
        self.api = get_config(FastApiSettings)
        self.database = get_config(DatabaseSettings)
        self.redis = get_config(RedisSettings)
