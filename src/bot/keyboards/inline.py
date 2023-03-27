from aiogram import types
from bot.keyboards.callback_enum import CallbackData, CallbakDataEnum, ObjectId, PageNavigator, Query
from bot.core import texts
from core.words.models import Word


add_favorite_keyboard = (
    types.InlineKeyboardMarkup()
    .add(
        types.InlineKeyboardButton(
            texts.add_to_favourites_text,
            callback_data=CallbackData(
                enum=CallbakDataEnum.save_favorite
            ).json()
        )
    )
)

remove_favorite_keyboard = (
    types.InlineKeyboardMarkup()
    .add(
        types.InlineKeyboardButton(
            texts.delete_from_favourites_text,
            callback_data=CallbackData(
                enum=CallbakDataEnum.remove_favorite,
            )
        )
    )
)

no_auth_start_keyboard = (
    types.InlineKeyboardMarkup()
    .add(
        types.InlineKeyboardButton(
            "Регистрация",
            callback_data=CallbackData[dict](
                enum=CallbakDataEnum.registration,
            ).json()
        )
    )
)


def generate_favorite_keyboard(favorite_words: list[Word], current_page: int = 0) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for word in favorite_words:
        markup.add(
            types.InlineKeyboardButton(
                word.text,
                callback_data=CallbackData[ObjectId](
                    enum=CallbakDataEnum.translate_word,
                    data=ObjectId(id=word.id),
                ).json()
            )
        )
    markup.add(
        types.InlineKeyboardButton(
            "Назад",
            callback_data=CallbackData[PageNavigator](
                enum=CallbakDataEnum.prev_page,
                data=PageNavigator(page_number=current_page-1),
            ).json()
        ),
        types.InlineKeyboardButton(
            "Вперед",
            callback_data=CallbackData[PageNavigator](
                enum=CallbakDataEnum.next_page,
                data=PageNavigator(page_number=current_page+1),
            ).json()
        ),
    )
    return markup


def generate_translate_keyboard(words: list[str]) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for word in words:
        markup.add(
            types.InlineKeyboardButton(
                word,
                callback_data=CallbackData(
                    enum=CallbakDataEnum.noop,
                ).json()
            )
        )
    return markup


auth_start_keyboard = None