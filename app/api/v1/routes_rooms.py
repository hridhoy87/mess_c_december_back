import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.database import get_session  
from app.api.v1.deps import get_current_user  

from app.models.building import Building  
from app.models.room_type import RoomType  
from app.models.room import Room  

from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingRead
from app.schemas.room_type import RoomTypeCreate, RoomTypeUpdate, RoomTypeRead
from app.schemas.room import RoomCreate, RoomUpdate, RoomRead

router = APIRouter(tags=["inventory"])

# -----------------
# Buildings
# -----------------
@router.get("/buildings", response_model=list[BuildingRead])
def list_buildings(
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
    active: bool | None = Query(default=None),
):
    stmt = select(Building)
    if active is not None:
        stmt = stmt.where(Building.is_active == active)
    return session.exec(stmt.order_by(Building.code)).all()

@router.post("/buildings", response_model=BuildingRead)
def create_building(
    data: BuildingCreate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    exists = session.exec(select(Building).where(Building.code == data.code)).first()
    if exists:
        raise HTTPException(status_code=409, detail="Building code already exists")

    b = Building.model_validate(data)
    session.add(b)
    session.commit()
    session.refresh(b)
    return b

@router.put("/buildings/{building_id}", response_model=BuildingRead)
def update_building(
    building_id: uuid.UUID,
    data: BuildingUpdate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    b = session.get(Building, building_id)
    if not b:
        raise HTTPException(status_code=404, detail="Building not found")

    patch = data.model_dump(exclude_unset=True)
    if "code" in patch:
        exists = session.exec(
            select(Building).where(Building.code == patch["code"], Building.id != building_id)
        ).first()
        if exists:
            raise HTTPException(status_code=409, detail="Building code already exists")

    for k, v in patch.items():
        setattr(b, k, v)

    session.add(b)
    session.commit()
    session.refresh(b)
    return b


# -----------------
# Room Types
# -----------------
@router.get("/room-types", response_model=list[RoomTypeRead])
def list_room_types(
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
    active: bool | None = Query(default=None),
):
    stmt = select(RoomType)
    if active is not None:
        stmt = stmt.where(RoomType.is_active == active)
    return session.exec(stmt.order_by(RoomType.name)).all()

@router.post("/room-types", response_model=RoomTypeRead)
def create_room_type(
    data: RoomTypeCreate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    # RoomType has no code; name is the practical unique handle. :contentReference[oaicite:13]{index=13}
    exists = session.exec(select(RoomType).where(RoomType.name == data.name)).first()
    if exists:
        raise HTTPException(status_code=409, detail="Room type name already exists")

    rt = RoomType.model_validate(data)
    session.add(rt)
    session.commit()
    session.refresh(rt)
    return rt

@router.put("/room-types/{room_type_id}", response_model=RoomTypeRead)
def update_room_type(
    room_type_id: uuid.UUID,
    data: RoomTypeUpdate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    rt = session.get(RoomType, room_type_id)
    if not rt:
        raise HTTPException(status_code=404, detail="Room type not found")

    patch = data.model_dump(exclude_unset=True)
    if "name" in patch:
        exists = session.exec(
            select(RoomType).where(RoomType.name == patch["name"], RoomType.id != room_type_id)
        ).first()
        if exists:
            raise HTTPException(status_code=409, detail="Room type name already exists")

    for k, v in patch.items():
        setattr(rt, k, v)

    session.add(rt)
    session.commit()
    session.refresh(rt)
    return rt


# -----------------
# Rooms
# -----------------
@router.get("/rooms", response_model=list[RoomRead])
def list_rooms(
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
    building_id: uuid.UUID | None = None,
    room_type_id: uuid.UUID | None = None,
    status: str | None = None,
    active: bool | None = None,
):
    stmt = select(Room)
    if building_id:
        stmt = stmt.where(Room.building_id == building_id)
    if room_type_id:
        stmt = stmt.where(Room.room_type_id == room_type_id)
    if status:
        stmt = stmt.where(Room.status == status)
    if active is not None:
        stmt = stmt.where(Room.is_active == active)

    return session.exec(stmt.order_by(Room.room_number)).all()

@router.post("/rooms", response_model=RoomRead)
def create_room(
    data: RoomCreate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    # Validate FK targets exist (prevents “abstract” junk)
    if not session.get(Building, data.building_id):
        raise HTTPException(status_code=400, detail="Invalid building_id")
    if not session.get(RoomType, data.room_type_id):
        raise HTTPException(status_code=400, detail="Invalid room_type_id")

    # Enforce uniqueness of room_number within building (common real-world rule)
    exists = session.exec(
        select(Room).where(Room.building_id == data.building_id, Room.room_number == data.room_number)
    ).first()
    if exists:
        raise HTTPException(status_code=409, detail="Room number already exists in this building")

    r = Room.model_validate(data)
    session.add(r)
    session.commit()
    session.refresh(r)
    return r

@router.put("/rooms/{room_id}", response_model=RoomRead)
def update_room(
    room_id: uuid.UUID,
    data: RoomUpdate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    r = session.get(Room, room_id)
    if not r:
        raise HTTPException(status_code=404, detail="Room not found")

    patch = data.model_dump(exclude_unset=True)

    if "room_type_id" in patch and patch["room_type_id"] is not None:
        if not session.get(RoomType, patch["room_type_id"]):
            raise HTTPException(status_code=400, detail="Invalid room_type_id")

    if "room_number" in patch and patch["room_number"] is not None:
        exists = session.exec(
            select(Room).where(
                Room.building_id == r.building_id,
                Room.room_number == patch["room_number"],
                Room.id != room_id,
            )
        ).first()
        if exists:
            raise HTTPException(status_code=409, detail="Room number already exists in this building")

    for k, v in patch.items():
        setattr(r, k, v)

    session.add(r)
    session.commit()
    session.refresh(r)
    return r
