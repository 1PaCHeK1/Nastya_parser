from aiogram import types
from bot.keyboards.callback_enum import BaseData, CallbakDataEnum, ObjectId, PageNavigator, Query
from bot.core import texts
from core.words.models import QuizQuestion, RightAnswerEnum, Word


add_favorite_keyboard = (
    types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=texts.add_to_favourites_text,
                    callback_data=BaseData(
                        enum=CallbakDataEnum.save_favorite
                    ).pack()
                )
            ],
        ]
    )
)


remove_favorite_keyboard = (
    types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=texts.delete_from_favourites_text,
                    callback_data=BaseData(
                        enum=CallbakDataEnum.remove_favorite,
                    ).pack()
                )
            ]
        ]
    )

)

no_auth_start_keyboard = (
    types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Регистрация",
                    callback_data=BaseData(
                        enum=CallbakDataEnum.registration,
                    ).pack()
                )
            ]
        ]
    )

)


def generate_favorite_keyboard(favorite_words: list[Word], current_page: int = 0) -> types.InlineKeyboardMarkup:
    buttons = []
    for word in favorite_words:
        buttons.append(
            types.InlineKeyboardButton(
                text=word.text,
                callback_data=BaseData(
                    enum=CallbakDataEnum.translate_word,
                    data=ObjectId(id=word.id),
                ).pack()
            )
        )
    buttons.extend(
        (
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=BaseData(
                    enum=CallbakDataEnum.prev_page,
                    data=PageNavigator(page_number=current_page-1),
                ).pack()
            ),
            types.InlineKeyboardButton(
                text="Вперед",
                callback_data=BaseData(
                    enum=CallbakDataEnum.next_page,
                    data=PageNavigator(page_number=current_page+1),
                ).pack()
            ),
        )
    )

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in buttons
        ]
    )


def generate_translate_keyboard(words: list[str]) -> types.InlineKeyboardMarkup:
    buttons = []
    for word in words:
        buttons.append(
            types.InlineKeyboardButton(
                word,
                callback_data=BaseData(
                    enum=CallbakDataEnum.noop,
                ).pack()
            )
        )

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in buttons
        ]
    )


auth_start_keyboard = None


def generate_question_keyboard(question: QuizQuestion):
    buttons = []
    for word, enum in [
        (question.answer_one, RightAnswerEnum.answer_one),
        (question.answer_two, RightAnswerEnum.answer_two),
        (question.answer_three, RightAnswerEnum.answer_three)
    ]:
        buttons.append(
            types.InlineKeyboardButton(
                word,
                callback_data=BaseData(
                    enum=CallbakDataEnum.quize_answer,
                    data=Query(text=enum.value),
                ).pack(),
            ),
        )
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in buttons
        ]
    )
