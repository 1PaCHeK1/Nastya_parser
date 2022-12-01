from .config import config
from aiogram import Bot, Dispatcher

bot = Bot(token=config.api_token)
dp = Dispatcher(bot)
