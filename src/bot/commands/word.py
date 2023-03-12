from contextlib import AbstractContextManager
from typing import Callable
from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.utils.auth import identify_user
from core.users.schemas import UserSchema
from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session

from bot.keyboards.callback_enum import CallbakDataEnum
from bot.core.dispatcher import dp

import bot.keyboards.inline as key_inline


from core.containers import Container
from core.caches.services import RedisService
from core.words.services import WordService


@dp.message_handler(Command("favorites"))
async def get_favorites(message: types.Message):
    fav_words = get_list_favorite()
    await message.answer("Список избранных слов:", ', '.join(fav_words))


@dp.message_handler(Command("list"))
@inject
async def get_list_word(
    message: types.Message,
    redis_service: RedisService = Provide[Container.redis_service]
):
    texts = (
        "\n".join(await redis_service.get_translations(message.from_id))
        or "Вы пока не ввели ни одного слова"
    )
    await message.answer(texts)


@dp.callback_query_handler()
async def callback(data: types.callback_query.CallbackQuery):
    match CallbakDataEnum(data.data):  # noqa: E999
        case CallbakDataEnum.save_favorite:
            await add_favorite(data)
        case CallbakDataEnum.remove_favorite:
            await remove_favorite(data)
        case _:
            ...


@identify_user
async def add_favorite(
        data:types.callback_query.CallbackQuery,
        user: UserSchema, 
        word_service: WordService = Provide[Container.word_service],
        get_session: Callable[..., AbstractContextManager[Session]] = Provide[Container.database.provided.session],
    ):
    word = data.message.reply_to_message.text
    translate = data.message.text
    with get_session() as session:
        word_service.add_favorite(word, user, session)
    await data.message.answer(f"Слово {word} записано в словарь с переводом {translate}")  # noqa: E501
    await data.message.edit_reply_markup(key_inline.remove_favorite_keyboard)


@identify_user
async def remove_favorite(
        data:types.callback_query.CallbackQuery,
        user: UserSchema, 
        word_service: WordService = Provide[Container.word_service],
        get_session: Callable[..., AbstractContextManager[Session]] = Provide[Container.database.provided.session],
    ):
    word = data.message.reply_to_message.text
    translate = data.message.text
    with get_session() as session:
        word_service.remove_favorite(word, user, session)
    await data.message.answer(f"Слово {word} удалено из словаря с переводом {translate}")  # noqa: E501
    await data.message.edit_reply_markup(key_inline.add_favorite_keyboard)


@identify_user
async def get_list_favorite(
        user: UserSchema, 
        word_service: WordService = Provide[Container.word_service],
        get_session: Callable[..., AbstractContextManager[Session]] = Provide[Container.database.provided.session],
    ):
    with get_session() as session:
        favorite_words = word_service.get_favorite(user, session)
    return favorite_words


@dp.message_handler()
@identify_user
@inject
async def translate_word(
    message: types.Message,
    user: UserSchema,
    word_service: WordService = Provide[Container.word_service],
    get_session: Callable[..., AbstractContextManager[Session]] = Provide[Container.database.provided.session],
):
    with get_session() as session:
        words = await word_service.get_translate(user, message.text, session)
    if words:
        words = ", ".join(words)
        await message.reply(words, reply_markup=key_inline.add_favorite_keyboard)
    else:
        await message.reply("Упс ничего не нашли")
