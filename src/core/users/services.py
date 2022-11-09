from .models import User 

class UserService:
    def __init__(self, session) -> None:
        self.session = session
    
    async def get_users(self) -> list[User]:
        return [1, 2, 3]
    
    async def get_user(self, id) -> User:
        return id+1

