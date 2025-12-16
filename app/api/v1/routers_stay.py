from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import uuid
from app.db.database import get_session
from app.models.stay import Stay
from app.models.reservation_room import ReservationRoom
from app.models.room import Room
from app.schemas.stay import StayCreate, StayRead, StayUpdate

router = APIRouter(prefix="/stays", tags=["stays"])


def _get_or_create_stay(session: Session, reservation_room_id):
    stay = session.exec(
        select(Stay).where(Stay.reservation_room_id == reservation_room_id)
    ).first()
    if stay:
        return stay

    stay = Stay(reservation_room_id=reservation_room_id)
    session.add(stay)
    session.flush()  # get stay.id without full commit
    return stay


@router.post("", response_model=StayRead)
def create_stay(
    data: StayCreate,
    session: Session = Depends(get_session),
):
    # data.reservation_room_id is the only valid key for Stay in your DB model
    rr = session.get(ReservationRoom, data.reservation_room_id)
    if not rr:
        raise HTTPException(status_code=404, detail="reservation_room not found")

    stay = _get_or_create_stay(session, rr.id)
    session.commit()
    session.refresh(stay)
    return stay


@router.post("/{reservation_room_id}/check-in", response_model=StayRead)
def check_in(
    reservation_room_id: uuid.UUID,
    session: Session = Depends(get_session),
):
    rr = session.get(ReservationRoom, reservation_room_id)
    if not rr:
        raise HTTPException(status_code=404, detail="reservation_room not found")

    if rr.room_id is None:
        raise HTTPException(status_code=409, detail="Room not assigned to reservation_room")

    room = session.get(Room, rr.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="room not found")

    stay = _get_or_create_stay(session, rr.id)

    # idempotency: if already checked in, just return current state
    if stay.status != "checked_in":
        stay.check_in_at = stay.check_in_at or datetime.utcnow()
        stay.status = "checked_in"
        room.status = "occupied"

    session.add(stay)
    session.add(room)
    session.commit()
    session.refresh(stay)
    return stay


@router.post("/{reservation_room_id}/check-out", response_model=StayRead)
def check_out(
    reservation_room_id: uuid.UUID,
    session: Session = Depends(get_session),
):
    rr = session.get(ReservationRoom, reservation_room_id)
    if not rr:
        raise HTTPException(status_code=404, detail="reservation_room not found")

    if rr.room_id is None:
        raise HTTPException(status_code=409, detail="Room not assigned to reservation_room")

    room = session.get(Room, rr.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="room not found")

    stay = session.exec(
        select(Stay).where(Stay.reservation_room_id == rr.id)
    ).first()
    if not stay:
        raise HTTPException(status_code=404, detail="stay not found")

    # idempotency: if already checked out, just return current state
    if stay.status != "checked_out":
        stay.check_out_at = stay.check_out_at or datetime.utcnow()
        stay.status = "checked_out"
        room.status = "available"

    session.add(stay)
    session.add(room)
    session.commit()
    session.refresh(stay)
    return stay


@router.patch("/{stay_id}", response_model=StayRead)
def update_stay(
    stay_id: uuid.UUID,
    data: StayUpdate,
    session: Session = Depends(get_session),
):
    stay = session.get(Stay, stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail="stay not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(stay, k, v)

    session.add(stay)
    session.commit()
    session.refresh(stay)
    return stay
