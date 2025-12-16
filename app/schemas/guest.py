# guest.py (schema file)
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel

class GuestCreate(SQLModel):
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


class GuestUpdate(SQLModel):
    ba_no: Optional[str] = None
    rk: Optional[str] = None
    full_name: Optional[str] = None

    unit: Optional[str] = None
    dt_of_req: Optional[date] = None

    id_card_no: Optional[str] = None
    pers_mobile_no: Optional[str] = None

    accompanying_num: Optional[int] = None
    spouse: Optional[bool] = None
    children: Optional[bool] = None

    car: Optional[bool] = None
    car_num: Optional[str] = None

    batman: Optional[bool] = None
    names_accompanying: Optional[str] = None

    purpose_of_use: Optional[str] = None
    alot_room: Optional[str] = None

    res_1: Optional[str] = None
    res_2: Optional[str] = None
    res_3: Optional[str] = None
    res_4: Optional[str] = None


class GuestReplace(SQLModel):
    # All fields required for full replacement (PUT)
    ba_no: Optional[str] = None
    rk: Optional[str] = None
    full_name: str  # Required

    unit: Optional[str] = None
    dt_of_req: Optional[date] = None

    id_card_no: Optional[str] = None
    pers_mobile_no: Optional[str] = None

    accompanying_num: int = 0  # Required with default
    spouse: bool = False  # Required with default
    children: bool = False  # Required with default

    car: bool = False  # Required with default
    car_num: Optional[str] = None

    batman: bool = False  # Required with default
    names_accompanying: Optional[str] = None

    purpose_of_use: Optional[str] = None
    alot_room: Optional[str] = None

    res_1: Optional[str] = None
    res_2: Optional[str] = None
    res_3: Optional[str] = None
    res_4: Optional[str] = None


class GuestRead(SQLModel):
    id: int  # BIGINT in DB
    ba_no: Optional[str]
    rk: Optional[str]
    full_name: str

    unit: Optional[str]
    dt_of_req: Optional[date]

    id_card_no: Optional[str]
    pers_mobile_no: Optional[str]

    accompanying_num: int
    spouse: bool
    children: bool

    car: bool
    car_num: Optional[str]

    batman: bool
    names_accompanying: Optional[str]

    purpose_of_use: Optional[str]
    alot_room: Optional[str]

    res_1: Optional[str]
    res_2: Optional[str]
    res_3: Optional[str]
    res_4: Optional[str]

    created_at: datetime