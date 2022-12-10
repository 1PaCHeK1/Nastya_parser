from aiogram import types
from bot.keyboards.callback_enum import CallbakDataEnum
from core import texts 

add_favorite_keyboard = (
    types.InlineKeyboardMarkup()
    .add(types.InlineKeyboardButton(texts.add_to_favourites_text, callback_data=CallbakDataEnum.save_favorite))
)

remove_favorite_keyboard = (
    types.InlineKeyboardMarkup()
    .add(types.InlineKeyboardButton(texts.delete_from_favourites_text, callback_data=CallbakDataEnum.remove_favorite))
)