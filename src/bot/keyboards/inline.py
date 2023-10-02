from aiogram import types

from bot.core import texts
from bot.keyboards.callback_enum import (
    BaseData,
    CallbackDataEnum,
    IdentCallBack,
    NavigationCallback,
    QueryCallBack,
)
from db.models import QuizQuestion, RightAnswerEnum, Word

add_favorite_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text=texts.add_to_favourites_text,
                callback_data=BaseData(enum=CallbackDataEnum.save_favorite).pack(),
            ),
        ],
    ],
)


remove_favorite_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text=texts.delete_from_favourites_text,
                callback_data=BaseData(
                    enum=CallbackDataEnum.remove_favorite,
                ).pack(),
            ),
        ],
    ],
)

no_auth_start_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Регистрация",
                callback_data=BaseData(
                    enum=CallbackDataEnum.registration,
                ).pack(),
            ),
        ],
    ],
)


def generate_favorite_keyboard(
    favorite_words: list[Word],
    current_page: int = 0,
) -> types.InlineKeyboardMarkup:
    buttons = []
    for word in favorite_words:
        buttons.append(
            types.InlineKeyboardButton(
                text=word.text,
                callback_data=IdentCallBack(
                    enum=CallbackDataEnum.translate_word,
                    data=word.id,
                ).pack(),
            ),
        )
    buttons.extend(
        (
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=NavigationCallback(
                    enum=CallbackDataEnum.prev_page,
                    data=current_page - 1,
                ).pack(),
            ),
            types.InlineKeyboardButton(
                text="Вперед",
                callback_data=NavigationCallback(
                    enum=CallbackDataEnum.next_page,
                    data=current_page + 1,
                ).pack(),
            ),
        ),
    )

    return types.InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])


def generate_translate_keyboard(words: list[str]) -> types.InlineKeyboardMarkup:
    buttons = []
    for word in words:
        buttons.append(
            types.InlineKeyboardButton(
                word,
                callback_data=BaseData(
                    enum=CallbackDataEnum.noop,
                ).pack(),
            ),
        )

    return types.InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])


auth_start_keyboard = None


def generate_question_keyboard(question: QuizQuestion):
    buttons = []
    for word, enum in [
        (question.answer_one, RightAnswerEnum.answer_one),
        (question.answer_two, RightAnswerEnum.answer_two),
        (question.answer_three, RightAnswerEnum.answer_three),
    ]:
        buttons.append(
            types.InlineKeyboardButton(
                text=word,
                callback_data=QueryCallBack(
                    enum=CallbackDataEnum.quize_answer,
                    data=enum.value,
                ).pack(),
            ),
        )
    return types.InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])


def generate_answer_keyboard(answer: str):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=answer,
                    callback_data=BaseData(
                        enum=CallbackDataEnum.noop,
                    ).pack(),
                ),
            ],
        ],
    )
