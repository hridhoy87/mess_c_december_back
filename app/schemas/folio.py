import uuid
from datetime import datetime
from sqlmodel import SQLModel

class FolioCreate(SQLModel):
    reservation_id: uuid.UUID
    opened_at: datetime | None = None  # if None, server sets now

class FolioUpdate(SQLModel):
    closed_at: datetime | None = None  # allow closing / reopening if you want

class FolioRead(SQLModel):
    id: uuid.UUID
    reservation_id: uuid.UUID
    opened_at: datetime
    closed_at: datetime | None
