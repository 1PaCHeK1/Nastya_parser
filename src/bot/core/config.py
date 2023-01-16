from pydantic import BaseSettings


class BotSettings(BaseSettings):
    api_token: str


class DevBotSettings(BotSettings):
    api_token = "5972795808:AAF9Sys9R230niLLnGmQ_KI6ywLQxBbFcmY"


class ProdBotSettings(BotSettings):
    class Meta:
        env_file = ".env"
