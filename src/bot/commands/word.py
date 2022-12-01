import json
from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.commands.callback_enum import CallbakDataEnum
from bot.core.dispatcher import dp


@dp.message_handler()
async def translate_word(message: types.Message):
    reply_markup = (types.ReplyKeyboardMarkup(resize_keyboard=True)
              .add(types.KeyboardButton("1"))
              .add(types.KeyboardButton("2"))
              .add(types.KeyboardButton("3"))
    )
    print(CallbakDataEnum.save_favorite.value)
    inline_markup = (
        types.InlineKeyboardMarkup()
        .add(types.InlineKeyboardButton("Добавить в избранное", callback_data=CallbakDataEnum.save_favorite))
    )
    await message.reply("Перевод", reply_markup=inline_markup)


@dp.message_handler(Command("favorites"))
async def get_favorites(message: types.Message):
    await message.answer("Список избранных слов")


@dp.message_handler(Command("list"))
async def get_list_word(message: types.Message):
    await message.answer("Список слов")


@dp.callback_query_handler()
async def callback(data:types.callback_query.CallbackQuery):
    match CallbakDataEnum(data.data):
        case CallbakDataEnum.save_favorite:
            await add_favorite(data)
        case CallbakDataEnum.remove_favorite:
            await remove_favorite(data)
        case _:
            ...


async def add_favorite(data:types.callback_query.CallbackQuery):
    word = data.message.reply_to_message.text
    translate = data.message.text
    inline_markup = (
        types.InlineKeyboardMarkup()
        .add(types.InlineKeyboardButton("Удалить из избранного", callback_data=CallbakDataEnum.remove_favorite))
    )
    await data.message.answer(f"Слово {word} записано в словарь с переводом {translate}")
    await data.message.edit_reply_markup(inline_markup)


async def remove_favorite(data:types.callback_query.CallbackQuery):
    word = data.message.reply_to_message.text
    translate = data.message.text
    inline_markup = (
        types.InlineKeyboardMarkup()
        .add(types.InlineKeyboardButton("Добавить в избранное", callback_data=CallbakDataEnum.save_favorite))
    )
    await data.message.answer(f"Слово {word} удалено из словаря с переводом {translate}")
    await data.message.edit_reply_markup(inline_markup)
