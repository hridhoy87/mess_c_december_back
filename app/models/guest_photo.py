import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class GuestPhoto(SQLModel, table=True):
    __tablename__ = "guest_photo"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    guest_id: int = Field(foreign_key="guest.id", index=True)

    object_key: str
    content_type: str
    byte_size: int
    sha256: Optional[str] = None

    captured_at: datetime = Field(default_factory=datetime.utcnow)
    captured_by_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user_account.id")

    note: Optional[str] = None
    is_primary: bool = False
