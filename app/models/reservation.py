import uuid
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Reservation(SQLModel, table=True):
    __tablename__ = "reservation"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    guest_id: int = Field(foreign_key="guest.id", index=True)

    check_in: date
    check_out: date

    status: str = Field(default="booked", index=True)  # booked/cancelled/no_show
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
