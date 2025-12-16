from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import BigInteger, Column

class Guest(SQLModel, table=True):
    __tablename__ = "guest"

    # auto increment BIGINT
    id: Optional[int] = Field(default=None, sa_column=Column(BigInteger, primary_key=True, autoincrement=True))

    ba_no: Optional[str] = None
    rk: Optional[str] = None
    full_name: str

    unit: Optional[str] = None
    dt_of_req: Optional[date] = None

    id_card_no: Optional[str] = None
    pers_mobile_no: Optional[str] = None

    accompanying_num: int = 0
    spouse: bool = False
    children: bool = False

    car: bool = False
    car_num: Optional[str] = None

    batman: bool = False
    names_accompanying: Optional[str] = None

    purpose_of_use: Optional[str] = None
    alot_room: Optional[str] = None

    res_1: Optional[str] = None
    res_2: Optional[str] = None
    res_3: Optional[str] = None
    res_4: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
