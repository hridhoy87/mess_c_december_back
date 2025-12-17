import uuid
from datetime import datetime
from sqlmodel import SQLModel

class RoomCreate(SQLModel):
    building_id: uuid.UUID
    room_type_id: uuid.UUID
    room_number: str
    floor: int | None = None
    status: str = "available"
    is_active: bool = True
    capacity: int = 2
    beds: str = "01xSemi Double"
    has_tv: bool = False
    has_ac: bool = False
    other_amenity: str | None = None
    # next_booking NOT in Create - it's auto-generated

class RoomUpdate(SQLModel):
    room_type_id: uuid.UUID | None = None
    room_number: str | None = None
    floor: int | None = None
    status: str | None = None
    is_active: bool | None = None
    capacity: int | None = None
    beds: str | None = None
    has_tv: bool | None = None
    has_ac: bool | None = None
    other_amenity: str | None = None
    # next_booking NOT in Update - it's auto-generated

class RoomRead(SQLModel):
    id: uuid.UUID
    building_id: uuid.UUID
    room_type_id: uuid.UUID
    room_number: str
    floor: int | None
    status: str
    is_active: bool
    capacity: int
    beds: str
    has_tv: bool
    has_ac: bool
    other_amenity: str | None
    # NEW FIELD - included in Read
    next_booking: datetime | None