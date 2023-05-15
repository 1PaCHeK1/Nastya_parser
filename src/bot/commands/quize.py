import json
from typing import Callable
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline import generate_answer_keyboard, generate_question_keyboard
from bot.utils.auth import RequiredUserFilter
from core.words.schemas import QuestionType
from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session
from aiogram.methods import EditMessageReplyMarkup
from sqlalchemy import update, select

from core.containers import Container
from core.users.schemas import UserSchema
from core.words.services import QuizeService, QuizeFilter
from core.words.models import QuizQuestion, QuizTheme
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
    Command("get_game_settings", ignore_case=True),
    RequiredUserFilter(),
)
@inject
async def get_game_settings(
    message: types.Message,
    user: UserSchema,
    get_session: Callable[[], Session] = Provide[Container.database.provided.session],
):
    with get_session() as session:
        q_filter = session.scalar(select(QuizeFilter).where(QuizeFilter.user.id == user.id))
        if not q_filter:
            q_filter = QuizeFilter(user=user)
            session.add(q_filter)
            session.flush()
        if q_filter.theme_id:
            theme = session.scalar(select(QuizTheme).where(QuizTheme.id==q_filter.theme_id))
            await message.answer("Тема:" + str(theme.name))
        else:
            await message.answer("Тема не выбрана")
        if q_filter.level:
            await message.answer("Уровень: " + str(q_filter.level))
        else:
            await message.answer("Уровень не выбран")
        await message.answer("Максимальное количество вопросов: " + str(q_filter.max_question))


@router.message(
    Command("change_maximum_quantity_of_questions", ignore_case=True),
    RequiredUserFilter(),
)
@inject
async def change_maximum_quantity_of_questions(
    message: types.Message,
    user: UserSchema,
    get_session: Callable[[], Session] = Provide[Container.database.provided.session],
):
    with get_session() as session:
        q_filter = session.scalar(select(QuizeFilter).where(QuizeFilter.user.id == user.id))
        if not q_filter:
            q_filter = QuizeFilter(user=user)
            session.add(q_filter)
            session.flush()

        if len(message.text.split()) != 2:
            await message.answer("Комманда введена неправильно, напишите /change_maximum_quantity_of_questions <кол-во вопросов>")
        else:
            try:
                stmt = update(QuizeFilter).where(QuizeFilter.user.id==user.id).values(max_question=int(message.text.split()[1]))
                await message.answer('Теперь максимальное количество вопросов равно ' + message.text.split()[1])
            except:
                await message.answer('Проверьте правильность ввода команды')


@router.message(
    Command("change_theme", ignore_case=True),
    RequiredUserFilter(),
)
@inject
async def change_theme(
    message: types.Message,
    user: UserSchema,
    get_session: Callable[[], Session] = Provide[Container.database.provided.session],
):
    with get_session() as session:
        q_filter = session.scalar(select(QuizeFilter).where(QuizeFilter.user.id == user.id))
        if not q_filter:
            q_filter = QuizeFilter(user=user)
            session.add(q_filter)
            session.flush()

        if len(message.text.split()) != 2:
            await message.answer("Комманда введена неправильно, напишите /change_theme <тема>")
        else:
            try:
                theme = session.scalar(select(QuizTheme).where(QuizTheme.name==message.text.split()[1]))
                stmt = update(QuizeFilter).where(QuizeFilter.user.id==user.id).values(theme_id=theme.id)
                session.execute(stmt)
                await message.answer('Теперь тема - ' + theme.name)
            except:
                await message.answer('Комманда введена неправильно или такой темы не существует')


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
):
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
