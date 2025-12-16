import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Folio(SQLModel, table=True):
    __tablename__ = "folio"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    reservation_id: uuid.UUID = Field(foreign_key="reservation.id", unique=True, index=True)

    opened_at: datetime = Field(default_factory=datetime.utcnow)
    closed_at: Optional[datetime] = None
