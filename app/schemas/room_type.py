import uuid
from sqlmodel import SQLModel

class RoomTypeCreate(SQLModel):
    name: str
    capacity: int = 1
    base_rate: float | None = None
    is_active: bool = True

class RoomTypeUpdate(SQLModel):
    name: str | None = None
    capacity: int | None = None
    base_rate: float | None = None
    is_active: bool | None = None

class RoomTypeRead(SQLModel):
    id: uuid.UUID
    name: str
    capacity: int
    base_rate: float | None
    is_active: bool
