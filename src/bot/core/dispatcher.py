from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from core.config import get_config


config = get_config()

bot = Bot(token=config.bot.api_token)
dp = Dispatcher(bot, storage=MemoryStorage())
