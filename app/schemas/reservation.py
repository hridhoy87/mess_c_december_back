import uuid
from datetime import date, datetime
from sqlmodel import SQLModel

class ReservationCreate(SQLModel):
    guest_id: int
    check_in: date
    check_out: date
    status: str = "booked"   # booked/cancelled/no_show
    notes: str | None = None

class ReservationUpdate(SQLModel):
    check_in: date | None = None
    check_out: date | None = None
    status: str | None = None
    notes: str | None = None

class ReservationRead(SQLModel):
    id: uuid.UUID
    guest_id: int
    check_in: date
    check_out: date
    status: str
    notes: str | None
    created_at: datetime
