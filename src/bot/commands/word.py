from contextlib import AbstractContextManager
import json
from typing import Callable
from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.utils.auth import identify_user, required_login
from core.users.schemas import UserSchema
from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session

from bot.keyboards.callback_enum import CallbackData, CallbakDataEnum, ObjectId, PageNavigator, Query
from bot.core.dispatcher import dp

import bot.keyboards.inline as key_inline


from core.containers import Container
from core.caches.services import RedisService
from core.words.services import WordService


@inject
async def get_translate(
    text: str,
    user: UserSchema,
    word_service: WordService = Provide[Container.word_service],
    get_session: Callable[..., AbstractContextManager[Session]] = Provide[Container.database.provided.session],
) -> list[str]:
    with get_session() as session:
        return await word_service.get_translate(user, text, session)


@dp.message_handler(Command("favorites"))
@required_login
async def get_favorites(
    message: types.Message,
    user: UserSchema,
):
    fav_words = await get_list_favorite(user)
    markup = key_inline.generate_favorite_keyboard(fav_words)
    await message.answer(f"Список избранных слов", reply_markup=markup)


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
@identify_user
async def callback(
    callback_info: types.callback_query.CallbackQuery,
    user: UserSchema,
):

    serialize_data = json.loads(callback_info.data)
    callback_data = CallbackData[dict].parse_obj(serialize_data)
    match CallbakDataEnum(callback_data.enum):  # noqa: E999
        case CallbakDataEnum.save_favorite:
            await add_favorite(callback_info)
        case CallbakDataEnum.remove_favorite:
            await remove_favorite(callback_info)
        case CallbakDataEnum.next_page | CallbakDataEnum.prev_page:
            callback_data = CallbackData[PageNavigator].parse_obj(serialize_data)
            favorite_list = await get_list_favorite(user, callback_data.data.page_number)
            markup = key_inline.generate_favorite_keyboard(favorite_list, callback_data.data.page_number)
            await callback_info.message.edit_reply_markup(markup)
        case CallbakDataEnum.translate_word:
            callback_data = CallbackData[Query].parse_obj(serialize_data)
            words = await get_translate(
                callback_data.data.text,
                user,
            )
            print(words)
            markup = key_inline.generate_translate_keyboard(words)
            await callback_info.message.edit_reply_markup(markup)


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


@inject
async def get_list_favorite(
    user: UserSchema,
    page_number: int = 0,
    word_service: WordService = Provide[Container.word_service],
    get_session: Callable[..., AbstractContextManager[Session]] = Provide[Container.database.provided.session],
):
    with get_session() as session:
        favorite_words = await word_service.get_favorite(user, page_number, session)
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
