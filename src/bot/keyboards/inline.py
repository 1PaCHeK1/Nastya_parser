from aiogram import types
from bot.keyboards.callback_enum import CallbakDataEnum
from bot.core import texts 

add_favorite_keyboard = (
    types.InlineKeyboardMarkup()
    .add(types.InlineKeyboardButton(
            texts.add_to_favourites_text, 
            callback_data=CallbakDataEnum.save_favorite.value
        )
    )
)

remove_favorite_keyboard = (
    types.InlineKeyboardMarkup()
    .add(types.InlineKeyboardButton(texts.delete_from_favourites_text, 
    callback_data=CallbakDataEnum.remove_favorite.value))
)

no_auth_start_keyboard = (
    types.InlineKeyboardMarkup()
    .add(types.InlineKeyboardButton("Регистрация", 
    callback_data=CallbakDataEnum.registration.value))
)

auth_start_keyboard = None