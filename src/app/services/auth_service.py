
from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, data: UserCreate) -> User:
        email = str(data.email).lower().strip()

        existing_user = await self.user_repository.get_user_by_email(email)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            name=data.name,
            last_name=data.last_name,
            email=email,
            password_hash=get_password_hash(data.password),
            rol="BASIC",
            active=True,
        )

        return await self.user_repository.create(user)

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_user_by_email(
            email.lower().strip()
        )

        if user is None or not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        access_token = create_access_token(subject=str(user.id))

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
