from typing import Annotated
from business_validator import ErrorSchema, ValidationError
from sqlalchemy.orm import Session
from api.auth import Authenticate
from api.router.bodies import UserRegistrationSchema, WordInsertWithTranslateSchema
from api.router.filters import WordFilterParams
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, Request
from aioinject import Inject
from aioinject.ext.fastapi import inject
from core.image.usecases import ReadTextFromImageUseCase
from core.users.schemas import UserRegistrationApiDto, UserSchema
from core.users.usecases import RegistrationFromApiUseCase
from core.words.dto import WordCoreFilter
from core.words.services import WordService
from core.words.schemas import WordCreateSchema
from api.schemas.word import WordSchema
from db.models import LanguageEnum


router = APIRouter(prefix="/auth")


@router.post("/registration")
@inject
async def registration(
    body: UserRegistrationSchema,
    usecase: Annotated[RegistrationFromApiUseCase, Inject]
) -> UserSchema:
    user = await usecase.execute(UserRegistrationApiDto.from_orm(body))
    if user is None:
        return HTTPException(status_code=400)

    return UserSchema.model_validate(user)


@router.post("/activation/{token}")
async def activation(
    token: Annotated[str, Path()],
) -> UserSchema:
    ...
