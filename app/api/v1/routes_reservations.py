import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_session
from app.api.v1.deps import get_current_user
from app.models.reservation import Reservation
from app.models.guest import Guest
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationRead

router = APIRouter(tags=["reservations"])

@router.get("/reservations", response_model=list[ReservationRead])
def list_reservations(
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    return session.exec(select(Reservation)).all()

@router.post("/reservations", response_model=ReservationRead)
def create_reservation(
    data: ReservationCreate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    if not session.get(Guest, data.guest_id):
        raise HTTPException(status_code=400, detail="Invalid guest_id")

    r = Reservation.model_validate(data)
    session.add(r)
    session.commit()
    session.refresh(r)
    return r

@router.put("/reservations/{reservation_id}", response_model=ReservationRead)
def update_reservation(
    reservation_id: uuid.UUID,
    data: ReservationUpdate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    r = session.get(Reservation, reservation_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(r, k, v)

    session.add(r)
    session.commit()
    session.refresh(r)
    return r
