import uuid
from datetime import datetime
from sqlmodel import SQLModel

class FolioItemCreate(SQLModel):
    stay_id: uuid.UUID | None = None
    kind: str
    description: str | None = None
    amount: float
    created_at: datetime | None = None

class FolioItemUpdate(SQLModel):
    kind: str | None = None
    description: str | None = None
    amount: float | None = None

class FolioItemRead(SQLModel):
    id: uuid.UUID
    folio_id: uuid.UUID
    stay_id: uuid.UUID | None
    kind: str
    description: str | None
    amount: float
    created_at: datetime
