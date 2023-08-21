from typing import Literal, TypeVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


TSettings = TypeVar("TSettings", bound=BaseSettings)


def get_settings(settings: type[TSettings]) -> TSettings:
    return settings()


class SentrySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="sentry_")

    dsn: str | None = None
    traces_sample_rate: float = 1.0


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db_")

    name: str = "localhost"
    host: str
    port: int = 5432
    user: str
    password: str

    echo: bool = True

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="redis_")

    host: str = "localhost"
    port: int = 6379
    url: str

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="app_")

    name: str = "Parser"
    debug: bool = True
    environment: Literal["local"] | Literal["dev"] | Literal["prod"]
    cert_file_path: str = ""


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="bot_")

    api_token: str

    webhook_host: str
    webhook_path: str
    webapp_host: str
    webapp_port: int



class FastApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="api_")


class ContainterSettings:
    sentry: SentrySettings
    app: AppSettings
    bot: BotSettings
    api: FastApiSettings
    database: DatabaseSettings
    redis: RedisSettings

    def __init__(self) -> None:
        self.sentry = get_settings(SentrySettings)
        self.app = get_settings(AppSettings)
        self.bot = get_settings(BotSettings)
        self.api = get_settings(FastApiSettings)
        self.database = get_settings(DatabaseSettings)
        self.redis = get_settings(RedisSettings)


class RabbitSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="rabbit_")

    host: str
    user: str
    password: str

    prefetch_count: int = 10

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}/"
