# routes_guests.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_session
from app.api.v1.deps import get_current_user
from app.models.guest import Guest
from app.schemas.guest import GuestCreate, GuestUpdate, GuestReplace, GuestRead

router = APIRouter(tags=["guests"])

@router.get("/guests", response_model=list[GuestRead])
def list_guests(
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    stmt = select(Guest)
    return session.exec(stmt.order_by(Guest.full_name)).all()

@router.get("/guests/{guest_id}", response_model=GuestRead)
def get_guest(
    guest_id: int,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    g = session.get(Guest, guest_id)
    if not g:
        raise HTTPException(status_code=404, detail="Guest not found")
    return g

@router.post("/guests", response_model=GuestRead)
def create_guest(
    data: GuestCreate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    g = Guest.model_validate(data)
    session.add(g)
    session.commit()
    session.refresh(g)
    return g

@router.put("/guests/{guest_id}", response_model=GuestRead)
def replace_guest(
    guest_id: int,
    data: GuestReplace,  # Use GuestReplace schema for PUT
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    g = session.get(Guest, guest_id)
    if not g:
        raise HTTPException(status_code=404, detail="Guest not found")

    # For PUT with GuestReplace, all fields are defined (booleans have defaults)
    for k, v in data.model_dump().items():
        setattr(g, k, v)

    session.add(g)
    session.commit()
    session.refresh(g)
    return g

@router.patch("/guests/{guest_id}", response_model=GuestRead)
def patch_guest(
    guest_id: int,
    data: GuestUpdate,  # Use GuestUpdate schema for PATCH
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    g = session.get(Guest, guest_id)
    if not g:
        raise HTTPException(status_code=404, detail="Guest not found")

    # For PATCH with GuestUpdate, only update provided fields
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(g, k, v)

    session.add(g)
    session.commit()
    session.refresh(g)
    return g