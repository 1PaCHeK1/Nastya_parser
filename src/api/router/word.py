from typing import Annotated
from business_validator import ErrorSchema, ValidationError
from sqlalchemy.orm import Session
from api.router.bodies import WordInsertWithTranslateSchema
from api.router.filters import WordFilterParams
from fastapi import APIRouter, Depends, UploadFile, Request
from dependency_injector.wiring import Provide, inject
from aioinject import Inject
from aioinject.ext.fastapi import inject as ai_inject
from core.containers import Container
from core.image.usecases import ReadTextFromImageUseCase
from core.words.dto import WordCoreFilter
from core.words.services import WordService
from core.words.schemas import WordCreateSchema
from api.schemas.word import WordSchema
from db.models import LanguageEnum


router = APIRouter(prefix="/word")


@router.get("/")
@inject
async def get_all_words(
    params: Annotated[WordFilterParams, Depends()],
    get_session_db = Depends(Provide[Container.database.provided.session]),
    word_service: WordService = Depends(Provide[Container.word_service]),
) -> list[WordSchema]:
    with get_session_db() as session:
        words = await word_service.get_words(
            WordCoreFilter(language=params.language, contain=params.contain),
            session,
        )

    return WordSchema.from_orm_list(words)


@router.get("/test")
@ai_inject
async def get_all_words_test(
    params: Annotated[WordFilterParams, Depends()],
    session: Annotated[Session, Inject],
    word_service: Annotated[WordService, Inject],
) -> list[WordSchema]:
    words = await word_service.get_words(
        WordCoreFilter(language=params.language, contain=params.contain),
        session,
    )
    return WordSchema.from_orm_list(words)


@router.get("/languages")
@inject
async def get_languages() -> list[str]:
    return [enum.name for enum in LanguageEnum]


@router.post("/")
@ai_inject
async def insert_word(
    body: WordInsertWithTranslateSchema,
    session: Annotated[Session, Inject],
    word_service: Annotated[WordService, Inject]
) -> None:
    word = {
        'word': body.text,
        'translate_words': [translate.text for translate in body.translates]
    }
    await word_service.append_word(WordCreateSchema.parse_obj(word), session)


@router.post("/translate-image")
@ai_inject
async def translate_image(
    upload_file: UploadFile,
    usecase: Annotated[ReadTextFromImageUseCase, Inject],
) -> str:
    result = await usecase.execute(upload_file)

    if isinstance(result, str):
        return result
    raise ValidationError[ErrorSchema](result)


@router.post("/stream")
@ai_inject
async def stream(
    request: Request,
) -> None:
    counter = 1
    async for chunk in request.stream():
        print()
        print(counter)
        counter += 1
        print()
