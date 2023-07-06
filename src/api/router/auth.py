from typing import Annotated
from starlette import status
from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import APIRouter
from sqlalchemy.orm import Session
from api.auth import Authenticate
from api.schemas.auth import SignInSchema, ResponseAuthSchema


router = APIRouter(prefix="/auth")


@router.post("/signin")
@inject
async def signin(
    body: SignInSchema,
    session: Annotated[Session, Inject],
) -> ResponseAuthSchema:
    ...


@router.post("/logout")
@inject
async def logout(
    token: Authenticate,
) -> None:
    ...


@router.get("/tokens")
@inject
async def get_all_tokens(
    token: Authenticate,
    session: Annotated[Session, Inject],
) -> list[str]:
    ...