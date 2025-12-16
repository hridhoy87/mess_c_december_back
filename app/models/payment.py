import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Payment(SQLModel, table=True):
    __tablename__ = "payment"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    folio_id: uuid.UUID = Field(foreign_key="folio.id", index=True)

    amount: float
    method: str = Field(default="cash")
    reference: Optional[str] = None

    received_by_user_id: uuid.UUID = Field(foreign_key="user_account.id", index=True)
    received_at: datetime = Field(default_factory=datetime.utcnow)
