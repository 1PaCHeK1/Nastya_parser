from collections.abc import Sequence

from db.models import Post, User

from .repository import PostRepository


class GetUnreadedPostQuery:
    def __init__(
        self,
        repository: PostRepository,
    ) -> None:
        self._repository = repository

    async def execute(self, user: User) -> Sequence[Post]:
        return await self._repository.get_unread_post(user)
