import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class ReservationRoom(SQLModel, table=True):
    __tablename__ = "reservation_room"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    reservation_id: uuid.UUID = Field(foreign_key="reservation.id", index=True)

    # optional until assigned
    room_type_id: Optional[uuid.UUID] = Field(default=None, foreign_key="room_type.id", index=True)
    room_id: Optional[uuid.UUID] = Field(default=None, foreign_key="room.id", index=True)

    occupants: int = 1
    rate: Optional[float] = None  # store fixed rate for audit

    status: str = Field(default="planned", index=True)  # planned/assigned/released
    created_at: datetime = Field(default_factory=datetime.utcnow)
