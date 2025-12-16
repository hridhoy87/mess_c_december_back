# routes_guest_photos.py
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_session
from app.api.v1.deps import get_current_user
from app.models.guest import Guest
from app.models.guest_photo import GuestPhoto
from app.schemas.guest_photo import GuestPhotoCreate, GuestPhotoUpdate, GuestPhotoRead

router = APIRouter(tags=["guest-photos"])

@router.get("/guests/{guest_id}/photos", response_model=list[GuestPhotoRead])
def list_guest_photos(
    guest_id: int,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    if not session.get(Guest, guest_id):
        raise HTTPException(status_code=404, detail="Guest not found")
    return session.exec(select(GuestPhoto).where(GuestPhoto.guest_id == guest_id)).all()

@router.post("/guests/{guest_id}/photos", response_model=GuestPhotoRead)
def create_guest_photo(
    guest_id: int,
    data: GuestPhotoCreate,
    session: Session = Depends(get_session),
    user = Depends(get_current_user),
):
    # Check if guest exists
    guest = session.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    # Get current user ID for captured_by_user_id
    captured_by_user_id = getattr(user, "id", None)
    if captured_by_user_id is None:
        raise HTTPException(status_code=500, detail="Authenticated user id missing")


    # Create the photo
    photo = GuestPhoto(
        guest_id=guest_id,  # From URL path
        object_key=data.object_key,
        content_type=data.content_type,
        byte_size=data.byte_size,
        sha256=data.sha256,
        captured_at=data.captured_at or datetime.utcnow(),
        captured_by_user_id=captured_by_user_id,  # From current user
        note=data.note,
        is_primary=data.is_primary,
    )

    session.add(photo)
    session.commit()
    session.refresh(photo)
    return photo

@router.get("/guest-photos/{photo_id}", response_model=GuestPhotoRead)
def get_guest_photo(
    photo_id: uuid.UUID,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    photo = session.get(GuestPhoto, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo

@router.patch("/guest-photos/{photo_id}", response_model=GuestPhotoRead)
def update_guest_photo(
    photo_id: uuid.UUID,
    data: GuestPhotoUpdate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    photo = session.get(GuestPhoto, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Only update provided fields
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(photo, k, v)

    session.add(photo)
    session.commit()
    session.refresh(photo)
    return photo

@router.delete("/guest-photos/{photo_id}", status_code=204)
def delete_guest_photo(
    photo_id: uuid.UUID,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    photo = session.get(GuestPhoto, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    session.delete(photo)
    session.commit()
    return None