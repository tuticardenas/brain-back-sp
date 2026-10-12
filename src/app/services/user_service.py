from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_users(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> list[User]:
        return await self.user_repository.get_all(
            limit=limit,
            offset=offset,
        )

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_user_by_id(user_id)
