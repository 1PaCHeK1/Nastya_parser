from typing import Annotated
from api.router.bodies import UserRegistrationSchema
from fastapi import APIRouter, HTTPException, Path
from aioinject import Inject
from aioinject.ext.fastapi import inject
from core.users.schemas import UserRegistrationApiDto, UserSchema
from core.users.usecases import RegistrationFromApiUseCase


router = APIRouter(prefix="/auth")


@router.post("/registration")
@inject
async def registration(
    body: UserRegistrationSchema, usecase: Annotated[RegistrationFromApiUseCase, Inject]
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
