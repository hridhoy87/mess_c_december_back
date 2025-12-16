import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.database import get_session
from app.api.v1.deps import get_current_user

from app.models.reservation_room import ReservationRoom
from app.models.reservation import Reservation
from app.models.room import Room
from app.models.room_type import RoomType

from app.schemas.reservation_room import (
    ReservationRoomCreate,
    ReservationRoomUpdate,
    ReservationRoomRead,
)

router = APIRouter(tags=["reservation-rooms"])


# -------------------------
# LIST (optionally filtered)
# -------------------------
@router.get("/reservation-rooms", response_model=list[ReservationRoomRead])
def list_reservation_rooms(
    session: Session = Depends(get_session),
    _user=Depends(get_current_user),
    reservation_id: uuid.UUID | None = Query(default=None),
):
    stmt = select(ReservationRoom)
    if reservation_id:
        stmt = stmt.where(ReservationRoom.reservation_id == reservation_id)
    return session.exec(stmt).all()


# ----------------------------------------
# CREATE (NESTED under reservation) ✅
# ----------------------------------------
@router.post(
    "/reservations/{reservation_id}/rooms",
    response_model=ReservationRoomRead,
)
def create_reservation_room(
    reservation_id: uuid.UUID,
    data: ReservationRoomCreate,
    session: Session = Depends(get_session),
    _user=Depends(get_current_user),
):
    # validate reservation
    if not session.get(Reservation, reservation_id):
        raise HTTPException(status_code=400, detail="Invalid reservation_id")

    # validate optional foreign keys
    if data.room_type_id and not session.get(RoomType, data.room_type_id):
        raise HTTPException(status_code=400, detail="Invalid room_type_id")

    if data.room_id and not session.get(Room, data.room_id):
        raise HTTPException(status_code=400, detail="Invalid room_id")

    rr = ReservationRoom(
        reservation_id=reservation_id,
        room_type_id=data.room_type_id,
        room_id=data.room_id,
        occupants=data.occupants,
        rate=data.rate,
        status=data.status,
        created_at=datetime.utcnow(),
    )

    session.add(rr)
    session.commit()
    session.refresh(rr)
    return rr


# -------------------------
# UPDATE
# -------------------------
@router.put("/reservation-rooms/{rr_id}", response_model=ReservationRoomRead)
def update_reservation_room(
    rr_id: uuid.UUID,
    data: ReservationRoomUpdate,
    session: Session = Depends(get_session),
    _user=Depends(get_current_user),
):
    rr = session.get(ReservationRoom, rr_id)
    if not rr:
        raise HTTPException(status_code=404, detail="ReservationRoom not found")

    patch = data.model_dump(exclude_unset=True)

    if "room_type_id" in patch and patch["room_type_id"] is not None:
        if not session.get(RoomType, patch["room_type_id"]):
            raise HTTPException(status_code=400, detail="Invalid room_type_id")

    if "room_id" in patch and patch["room_id"] is not None:
        if not session.get(Room, patch["room_id"]):
            raise HTTPException(status_code=400, detail="Invalid room_id")

    for k, v in patch.items():
        setattr(rr, k, v)

    session.add(rr)
    session.commit()
    session.refresh(rr)
    return rr
