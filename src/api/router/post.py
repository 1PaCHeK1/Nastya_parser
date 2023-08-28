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
from core.posts.query import GetUnreadedPostQuery
from core.users.schemas import UserRegistrationApiDto, UserSchema
from core.users.usecases import RegistrationFromApiUseCase
from core.words.dto import WordCoreFilter
from core.words.services import WordService
from core.words.schemas import WordCreateSchema
from api.schemas.word import WordSchema
from db.models import LanguageEnum


router = APIRouter(prefix="/posts")


@router.get("/unread")
@inject
async def get_unread_posts(
    query: Annotated[GetUnreadedPostQuery, Inject],
    token: Authenticate,
) -> list[str]:
    posts = await query.execute(token.user)
    return [
        post.title
        for post in posts
    ]
