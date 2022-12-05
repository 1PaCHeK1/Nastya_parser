from aiogram import types
from bot.keyboards.callback_enum import CallbakDataEnum


add_favorite_keyboard = (
    types.InlineKeyboardMarkup()
    .add(types.InlineKeyboardButton("Добавить в избранное", callback_data=CallbakDataEnum.save_favorite))
)

remove_favorite_keyboard = (
    types.InlineKeyboardMarkup()
    .add(types.InlineKeyboardButton("Удалить из избранного", callback_data=CallbakDataEnum.remove_favorite))
)