from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthenticatedUser(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    rol: str
    active: bool

    model_config = ConfigDict(from_attributes=True)
