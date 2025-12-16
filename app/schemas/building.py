import uuid
from sqlmodel import SQLModel

class BuildingCreate(SQLModel):
    code: str
    name: str
    is_active: bool = True

class BuildingUpdate(SQLModel):
    code: str | None = None
    name: str | None = None
    is_active: bool | None = None

class BuildingRead(SQLModel):
    id: uuid.UUID
    code: str
    name: str
    is_active: bool
