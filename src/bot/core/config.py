from pydantic import BaseSettings

try:    from .local import environment
except: environment = "dev"


class Settings(BaseSettings):
    api_token: str


class DevSettings(Settings):
    api_token = "5972795808:AAF9Sys9R230niLLnGmQ_KI6ywLQxBbFcmY"


class ProdSettings(Settings):
    class Meta:
        env_file = ".env"


if environment == "dev":
    config = DevSettings()
if environment == "prod":
    config = ProdSettings()
