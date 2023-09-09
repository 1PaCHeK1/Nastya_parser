from typing import Annotated

from aioinject import Inject
from aioinject.ext.fastapi import inject
from business_validator import ErrorSchema, ValidationError
from fastapi import APIRouter, Depends, Request, UploadFile

from api.auth import Authenticate
from api.router.bodies import WordInsertWithTranslateSchema
from api.router.filters import WordFilterParams
from api.schemas.word import WordSchema
from core.image.usecases import ReadTextFromImageUseCase
from core.words.dto import WordCoreFilter
from core.words.schemas import WordCreateSchema
from core.words.services import WordService
from db.models import LanguageEnum

router = APIRouter(prefix="/word")


@router.get("/words")
@inject
async def get_all_words(
    token: Authenticate,
    params: Annotated[WordFilterParams, Depends()],
    word_service: Annotated[WordService, Inject],
) -> list[WordSchema]:
    words = await word_service.get_words(WordCoreFilter(language=params.language, contain=params.contain))
    return WordSchema.model_validate_list(words)


@router.get("/languages")
@inject
async def get_languages() -> list[str]:
    return [enum.name for enum in LanguageEnum]


@router.post("/")
@inject
async def insert_word(
    body: WordInsertWithTranslateSchema,
    word_service: Annotated[WordService, Inject],
) -> None:
    word = {
        "word": body.text,
        "translate_words": [translate.text for translate in body.translates],
    }
    await word_service.append_word(WordCreateSchema.parse_obj(word))


@router.post("/translate-image")
@inject
async def translate_image(
    upload_file: UploadFile,
    usecase: Annotated[ReadTextFromImageUseCase, Inject],
) -> str:
    result = await usecase.execute(upload_file)

    if isinstance(result, str):
        return result
    raise ValidationError[ErrorSchema](result)


@router.post("/stream")
@inject
async def stream(
    request: Request,
) -> None:
    counter = 1
    async for chunk in request.stream():
        print()
        print(counter)
        counter += 1
        print()
