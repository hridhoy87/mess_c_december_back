import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class FolioItem(SQLModel, table=True):
    __tablename__ = "folio_item"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    folio_id: uuid.UUID = Field(foreign_key="folio.id", index=True)

    # optional breakdown per room-stay
    stay_id: Optional[uuid.UUID] = Field(default=None, foreign_key="stay.id", index=True)

    kind: str
    description: Optional[str] = None
    amount: float

    created_at: datetime = Field(default_factory=datetime.utcnow)
