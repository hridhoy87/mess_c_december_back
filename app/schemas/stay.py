import uuid
from datetime import datetime
from sqlmodel import SQLModel

class StayCreate(SQLModel):
    reservation_room_id: uuid.UUID

class StayUpdate(SQLModel):
    check_in_at: datetime | None = None
    check_out_at: datetime | None = None
    status: str | None = None  # expected/checked_in/checked_out

class StayRead(SQLModel):
    id: uuid.UUID
    reservation_room_id: uuid.UUID
    check_in_at: datetime | None
    check_out_at: datetime | None
    status: str
