from .config import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
bot = Bot(token=config.api_token)
dp = Dispatcher(bot, storage=MemoryStorage())
