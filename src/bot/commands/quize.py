from contextlib import AbstractContextManager
import json
import re
from typing import Any, Callable
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline import generate_question_keyboard
from bot.utils.auth import required_login
from pydantic import BaseModel, BaseConfig
from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session

from core.containers import Container
from core.users.schemas import UserCreateSchema, UserSchema
from core.users.services import UserService
from core.words.services import QuizeService, QuizeFilter
from core.words.models import QuizQuestion
from bot.keyboards.callback_enum import CallbackData, CallbakDataEnum, Query
from bot.core.dispatcher import dp


class QuestionType(BaseModel):
    question: str
    answer_one: str
    answer_two: str
    answer_three: str
    right_answer: str

    class Config(BaseConfig):
        orm_mode = True

    @classmethod
    def from_orm_list(cls, objs: list[Any]) -> list["QuestionType"]:
        return [QuestionType.from_orm(obj) for obj in objs]

    @classmethod
    def parse_obj_list(cls, objs: list[Any]) -> list["QuestionType"]:
        return [QuestionType.parse_obj(obj) for obj in objs]


async def send_question(
    message: types.Message,
    question: QuizQuestion
) -> None:
    await message.answer(
        question.question,
        reply_markup=generate_question_keyboard(question),
    )


@dp.message_handler(Command("quize", ignore_case=True))
@required_login
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


@dp.callback_query_handler(state=["quize-game"])
@required_login
@inject
async def send_answer(
    query: types.CallbackQuery,
    user: UserSchema,
    state: FSMContext,
) -> None:

    data = await state.get_data()
    query_data = CallbackData[Query].parse_obj(json.loads(query.data))
    data["answers"].append(query_data.data.text)
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
        await state.finish()
