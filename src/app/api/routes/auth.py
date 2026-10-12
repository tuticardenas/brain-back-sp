
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthenticatedUser, TokenResponse, UserCreate
from app.services.auth_service import AuthService


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuthService:
    repository = UserRepository(db)
    return AuthService(repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@auth_router.post(
    "/register",
    response_model=AuthenticatedUser,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
)
async def register_user(
    data: UserCreate,
    service: AuthServiceDep,
):
    return await service.register_user(data)


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
):
    return await service.login(
        email=form_data.username,
        password=form_data.password,
    )
