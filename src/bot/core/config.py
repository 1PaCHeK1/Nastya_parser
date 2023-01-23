from pydantic import BaseSettings


class BotSettings(BaseSettings):
    api_token: str

    webhook_host: str
    webhook_path: str
    webapp_host: str
    webapp_port: int


class DevBotSettings(BotSettings):
    api_token = "5972795808:AAF9Sys9R230niLLnGmQ_KI6ywLQxBbFcmY"

    webhook_host: str = ""
    webhook_path: str = ""
    webapp_host: str = ""
    webapp_port: int = 0


class ProdBotSettings(BotSettings):
    class Meta:
        env_file = ".env"
