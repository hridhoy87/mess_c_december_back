import uuid
from typing import Optional
from datetime import datetime
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
    
    # Amenities
    capacity: int = Field(default=2)
    beds: str = Field(default="01xSemi Double")
    has_tv: bool = Field(default=False)
    has_ac: bool = Field(default=False)
    other_amenity: Optional[str] = None
    
    # NEW FIELD - Automatically updated by trigger
    next_booking: Optional[datetime] = None