from aiogram import types
from bot.keyboards.callback_enum import CallbackData, CallbakDataEnum
from bot.core import texts
from core.words.models import Word


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


def generate_favorite_keyboard(favorite_words: list[Word]) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for word in favorite_words:
        markup.add(
            types.InlineKeyboardButton(
                word.text,
                callback_data=CallbackData(
                    enum=CallbakDataEnum.favorite_word,
                    data=word.id,
                ).to_json()
            )
        )
    return markup


auth_start_keyboard = None