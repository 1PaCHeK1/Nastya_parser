from collections.abc import Sequence
from .repository import PostRepository

from db.models import User, Post


class GetUnreadedPostQuery:
    def __init__(
        self,
        repository: PostRepository,
    ) -> None:
        self._repository = repository

    async def execute(self, user: User) -> Sequence[Post]:
        return await self._repository.get_unread_post(user)
