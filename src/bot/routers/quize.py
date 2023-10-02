from typing import Annotated

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import EditMessageReplyMarkup
from aioinject import Inject
from aioinject.ext.fastapi import inject

from bot.filters.auth import RequiredUserFilter
from bot.keyboards.callback_enum import QueryCallBack
from bot.keyboards.inline import generate_answer_keyboard, generate_question_keyboard
from core.users.schemas import UserSchema
from core.words.schemas import QuestionType
from core.words.services import QuizeService
from db.models import QuizQuestion

router = Router(name="quize")


async def send_question(message: types.Message, question: QuizQuestion) -> None:
    await message.answer(
        question.question,
        reply_markup=generate_question_keyboard(question),
    )


@router.message(
    Command("get_game_settings", ignore_case=True),
    RequiredUserFilter(),
)
@inject
async def get_game_settings(
    message: types.Message,
    user: UserSchema,
    quize_service: Annotated[QuizeService, Inject],
):
    q_filter = await quize_service.get_filter_by_user(user)
    if q_filter.theme_id:
        theme = await quize_service.get_quize_theme_by_id(q_filter.theme_id)
        await message.answer("Тема:" + str(theme.name))
    else:
        await message.answer("Тема не выбрана")
    if q_filter.level:
        await message.answer("Уровень: " + str(q_filter.level))
    else:
        await message.answer("Уровень не выбран")
    await message.answer(
        "Максимальное количество вопросов: " + str(q_filter.max_question),
    )


@router.message(
    Command("change_maximum_quantity_of_questions", ignore_case=True),
    RequiredUserFilter(),
)
@inject
async def change_maximum_quantity_of_questions(
    message: types.Message,
    user: UserSchema,
    quize_service: Annotated[QuizeService, Inject],
):
    if len(message.text.split()) != 2:
        await message.answer(
            "Комманда введена неправильно, напишите /change_maximum_quantity_of_questions <кол-во вопросов>",
        )
    else:
        try:
            quize_service.update_filter_data(
                user, {"max_question": int(message.text.split()[1])}
            )
        except:
            await message.answer("Проверьте правильность ввода команды")
        else:
            await message.answer(
                "Теперь максимальное количество вопросов равно "
                + message.text.split()[1],
            )


@router.message(
    Command("change_theme", ignore_case=True),
    RequiredUserFilter(),
)
@inject
async def change_theme(
    message: types.Message,
    user: UserSchema,
    quize_service: Annotated[QuizeService, Inject],
):
    if len(message.text.split()) != 2:
        await message.answer(
            "Комманда введена неправильно, напишите /change_theme <тема>",
        )
    else:
        try:
            theme = await quize_service.get_quize_theme_by_name(message.text.split()[1])
            await quize_service.update_filter_data(user, {"theme_id": theme.id})
        except:
            await message.answer(
                "Комманда введена неправильно или такой темы не существует",
            )
        else:
            await message.answer("Теперь тема - " + theme.name)


@router.message(
    Command("quize", ignore_case=True),
    RequiredUserFilter(),
)
@inject
async def start_game(
    message: types.Message,
    user: UserSchema,
    state: FSMContext,
    quize_service: Annotated[QuizeService, Inject],
):
    quize_quest = await quize_service.get_game(user)

    if len(quize_quest) == 0:
        return

    await state.set_state("quize-game")
    serialize_data = [obj for obj in QuestionType.from_orm_list(quize_quest)]
    await state.set_data(
        {
            "position": 0,
            "questions": list(map(QuestionType.dict, serialize_data)),
            "answers": [],
        },
    )
    await send_question(message, quize_quest[0])


@router.callback_query(
    RequiredUserFilter(),
)
@inject
async def send_answer(
    query: types.CallbackQuery,
    user: UserSchema,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    query_data = QueryCallBack.unpack(query.data)
    data["answers"].append(query_data.data)
    await EditMessageReplyMarkup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=generate_answer_keyboard("Ответ засчитан!"),
    )
    if len(data["questions"]) > data["position"] + 1:
        next_question = QuestionType.parse_obj(data["questions"][data["position"] + 1])
        await send_question(query.message, next_question)
        await state.set_data(
            {
                "position": data["position"] + 1,
                "questions": data["questions"],
                "answers": data["answers"],
            },
        )
    else:
        score = 0
        for question, answer in zip(data["questions"], data["answers"]):
            score += question["right_answer"] == answer
        await query.message.answer(f"Ты набрал {score} очков!")
        await state.clear()
