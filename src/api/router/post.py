from typing import Annotated
from api.auth import Authenticate
from fastapi import APIRouter
from aioinject import Inject
from aioinject.ext.fastapi import inject
from core.posts.query import GetUnreadedPostQuery


router = APIRouter(prefix="/posts")


@router.get("/unread")
@inject
async def get_unread_posts(
    query: Annotated[GetUnreadedPostQuery, Inject],
    token: Authenticate,
) -> list[str]:
    posts = await query.execute(token.user)
    return [post.title for post in posts]
