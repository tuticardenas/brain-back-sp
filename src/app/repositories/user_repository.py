from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> list[User]:
        statement = (
            select(User)
            .order_by(User.id)
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(statement)

        return list(result.scalars().all())