from typing import Annotated
from api.router.bodies import WordInsertWithTranslateSchema
from api.router.filters import WordFilterParams
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from core.containers import Container
from core.words.dto import WordCoreFilter
from core.words.services import WordService
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


@router.get("/languages")
@inject
async def get_languages() -> list[str]:
    return [enum.name for enum in LanguageEnum]


@router.post("/")
async def insert_word(body: WordInsertWithTranslateSchema) -> None:
    print(body)
