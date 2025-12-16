import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Stay(SQLModel, table=True):
    __tablename__ = "stay"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    reservation_room_id: uuid.UUID = Field(foreign_key="reservation_room.id", unique=True, index=True)

    check_in_at: Optional[datetime] = None
    check_out_at: Optional[datetime] = None

    status: str = Field(default="expected", index=True)  # expected/checked_in/checked_out
