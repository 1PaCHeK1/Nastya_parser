from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from core.containers import Container
from core.words.services import WordService
from api.schemas.word import WordSchema


router = APIRouter(prefix="/word")


@router.get("/all")
@inject
async def get_all_words(
    get_session_db = Depends(Provide[Container.database.provided.session]),
    word_service: WordService = Depends(Provide[Container.word_service]),
) -> list[WordSchema]:
    with get_session_db() as session:
        words = await word_service.get_words(session)

    return WordSchema.from_orm_list(words)
