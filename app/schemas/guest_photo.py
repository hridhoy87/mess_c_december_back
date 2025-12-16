# guest_photo.py (schema file)
import uuid
from datetime import datetime
from sqlmodel import SQLModel

class GuestPhotoCreate(SQLModel):
    # REMOVE guest_id from here - it comes from URL path
    object_key: str
    content_type: str
    byte_size: int
    sha256: str | None = None
    captured_at: datetime | None = None  # if None, server sets now
    note: str | None = None
    is_primary: bool = False


class GuestPhotoUpdate(SQLModel):
    note: str | None = None
    is_primary: bool | None = None
    sha256: str | None = None
    # Can also update captured_by_user_id if needed


class GuestPhotoRead(SQLModel):
    id: uuid.UUID
    guest_id: int
    object_key: str
    content_type: str
    byte_size: int
    sha256: str | None
    captured_at: datetime
    captured_by_user_id: uuid.UUID | None
    note: str | None
    is_primary: bool