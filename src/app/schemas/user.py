from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    rol: str
    created_at: datetime
    updated_at: datetime | None
    active: bool

    model_config = ConfigDict(from_attributes=True)
