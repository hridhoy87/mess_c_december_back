import uuid
from sqlmodel import SQLModel, Field

class RoomType(SQLModel, table=True):
    __tablename__ = "room_type"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str = Field(index=True)
    capacity: int = 1
    base_rate: float | None = None
    is_active: bool = True
