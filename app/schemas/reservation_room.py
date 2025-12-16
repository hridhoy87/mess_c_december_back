import uuid
from datetime import datetime
from sqlmodel import SQLModel

class ReservationRoomCreate(SQLModel):
    room_type_id: uuid.UUID | None = None
    room_id: uuid.UUID | None = None
    occupants: int = 1
    rate: float | None = None
    status: str = "clean" # e.g., clean, dirty, maintenance

class ReservationRoomUpdate(SQLModel):
    room_type_id: uuid.UUID | None = None
    room_id: uuid.UUID | None = None
    occupants: int | None = None
    rate: float | None = None
    status: str | None = None

class ReservationRoomRead(SQLModel):
    id: uuid.UUID
    reservation_id: uuid.UUID
    room_type_id: uuid.UUID | None
    room_id: uuid.UUID | None
    occupants: int
    rate: float | None
    status: str
    created_at: datetime
