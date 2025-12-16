import uuid
from sqlmodel import SQLModel

class RoomCreate(SQLModel):
    building_id: uuid.UUID
    room_type_id: uuid.UUID
    room_number: str
    floor: int | None = None
    status: str = "available"
    is_active: bool = True

class RoomUpdate(SQLModel):
    room_type_id: uuid.UUID | None = None
    room_number: str | None = None
    floor: int | None = None
    status: str | None = None
    is_active: bool | None = None

class RoomRead(SQLModel):
    id: uuid.UUID
    building_id: uuid.UUID
    room_type_id: uuid.UUID
    room_number: str
    floor: int | None
    status: str
    is_active: bool
