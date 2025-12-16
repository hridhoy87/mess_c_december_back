# payment.py (schema file)
import uuid
from datetime import datetime
from sqlmodel import SQLModel

class PaymentCreate(SQLModel):
    amount: float
    method: str
    reference: str | None = None
    received_at: datetime | None = None


class PaymentRead(SQLModel):
    id: uuid.UUID
    folio_id: uuid.UUID
    amount: float
    method: str
    reference: str | None
    received_by_user_id: uuid.UUID
    received_at: datetime