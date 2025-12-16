import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field

class UserAccount(SQLModel, table=True):
    __tablename__ = "user_account"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="frontdesk", index=True)  # admin/manager/frontdesk/housekeeping
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
