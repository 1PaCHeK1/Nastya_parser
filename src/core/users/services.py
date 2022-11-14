from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session

from .models import User 

class UserService:
    def __init__(self, session:Callable[..., AbstractContextManager[Session]]) -> None:
        self.session = session
    
    async def get_users(self) -> list[User]:
        with self.session() as db:
            print(db.query(User).all())
            return db.query(User).all()
    
    async def get_user(self, id) -> User:
        return id+1

