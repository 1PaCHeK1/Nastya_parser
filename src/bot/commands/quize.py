import json
from typing import Callable
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline import generate_answer_keyboard, generate_question_keyboard
from bot.utils.auth import RequiredUserFilter
from core.words.schemas import QuestionType
from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session
from aiogram.methods import EditMessageReplyMarkup

from core.containers import Container
from core.users.schemas import UserSchema
from core.words.services import QuizeService
from core.words.models import QuizQuestion
from bot.keyboards.callback_enum import BaseData, CallbakDataEnum, QueryCallBack


router = Router()


async def send_question(
    message: types.Message,
    question: QuizQuestion
) -> None:
    await message.answer(
        question.question,
        reply_markup=generate_question_keyboard(question),
    )


@router.message(
    Command("quize", ignore_case=True),
    RequiredUserFilter(),
)
@inject
async def start_game(
    message: types.Message,
    user: UserSchema,
    state: FSMContext,
    get_session: Callable[[], Session] = Provide[Container.database.provided.session],
    quize_service: QuizeService = Provide[Container.quize_service],
) -> None:
    with get_session() as session:
        quize_quest = await quize_service.get_game(user, session)
        if len(quize_quest) == 0:
            return

        await state.set_state("quize-game")
        serialize_data = [obj for obj in QuestionType.from_orm_list(quize_quest)]
        await state.set_data(
            {
                "position": 0,
                "questions": list(map(QuestionType.dict, serialize_data)),
                "answers": [],
            }
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
        reply_markup=generate_answer_keyboard("Ответ засчитан!")
    )
    if len(data["questions"]) > data["position"] + 1:
        next_question = QuestionType.parse_obj(data["questions"][data["position"] + 1])
        await send_question(query.message, next_question)
        await state.set_data(
            {
                "position": data["position"] + 1,
                "questions": data["questions"],
                "answers": data["answers"],
            }
        )
    else:
        score = 0
        for question, answer in zip(data["questions"], data["answers"]):
            score += question["right_answer"] == answer
        await query.message.answer(f"Ты набрал {score} очков!")
        await state.clear()
