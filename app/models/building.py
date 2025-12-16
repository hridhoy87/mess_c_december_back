import uuid
from sqlmodel import SQLModel, Field

class Building(SQLModel, table=True):
    __tablename__ = "building"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    code: str = Field(index=True, unique=True)
    name: str
    is_active: bool = True
