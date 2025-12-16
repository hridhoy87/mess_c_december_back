import uuid
from typing import Optional
from sqlmodel import SQLModel, Field

class Room(SQLModel, table=True):
    __tablename__ = "room"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    building_id: uuid.UUID = Field(foreign_key="building.id", index=True)
    room_type_id: uuid.UUID = Field(foreign_key="room_type.id", index=True)

    room_number: str = Field(index=True)
    floor: Optional[int] = None

    status: str = Field(default="available", index=True)  # available/occupied/cleaning/maintenance
    is_active: bool = True
