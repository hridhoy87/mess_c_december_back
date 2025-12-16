import uuid
from datetime import datetime
from sqlmodel import SQLModel

class UserAccountRead(SQLModel):
    id: uuid.UUID
    email: str
    role: str
    is_active: bool
    created_at: datetime

class UserAccountUpdate(SQLModel):
    role: str | None = None
    is_active: bool | None = None
