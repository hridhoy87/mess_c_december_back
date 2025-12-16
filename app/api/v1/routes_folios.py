from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.database import get_session
from app.api.v1.deps import get_current_user

from app.models.folio import Folio
from app.models.folio_item import FolioItem
from app.models.reservation import Reservation
from app.models.stay import Stay

from app.schemas.folio import FolioCreate, FolioUpdate, FolioRead
from app.schemas.folio_item import FolioItemCreate, FolioItemUpdate, FolioItemRead

router = APIRouter(tags=["folio"])


# ---- Folios ----
@router.get("/folios", response_model=list[FolioRead])
def list_folios(
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
    reservation_id: uuid.UUID | None = Query(default=None),
):
    stmt = select(Folio)
    if reservation_id:
        stmt = stmt.where(Folio.reservation_id == reservation_id)
    return session.exec(stmt).all()


@router.post("/folios", response_model=FolioRead)
def create_folio(
    data: FolioCreate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    # Ensure reservation exists
    if not session.get(Reservation, data.reservation_id):
        raise HTTPException(status_code=400, detail="Invalid reservation_id")

    # Enforce 1 folio per reservation (DB already has UNIQUE index; we guard early)
    existing = session.exec(
        select(Folio).where(Folio.reservation_id == data.reservation_id)
    ).first()
    if existing:
        return existing

    opened_at = data.opened_at or datetime.utcnow()
    f = Folio(reservation_id=data.reservation_id, opened_at=opened_at, closed_at=None)

    session.add(f)
    session.commit()
    session.refresh(f)
    return f


@router.put("/folios/{folio_id}", response_model=FolioRead)
def update_folio(
    folio_id: uuid.UUID,
    data: FolioUpdate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    f = session.get(Folio, folio_id)
    if not f:
        raise HTTPException(status_code=404, detail="Folio not found")

    patch = data.model_dump(exclude_unset=True)
    for k, v in patch.items():
        setattr(f, k, v)

    session.add(f)
    session.commit()
    session.refresh(f)
    return f


# ---- Folio Items ----
@router.get("/folios/{folio_id}/items", response_model=list[FolioItemRead])
def list_items(
    folio_id: uuid.UUID,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    if not session.get(Folio, folio_id):
        raise HTTPException(status_code=404, detail="Folio not found")
    return session.exec(select(FolioItem).where(FolioItem.folio_id == folio_id)).all()


@router.post("/folios/{folio_id}/items", response_model=FolioItemRead)
def add_item(
    folio_id: uuid.UUID,
    data: FolioItemCreate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    f = session.get(Folio, folio_id)
    if not f:
        raise HTTPException(status_code=404, detail="Folio not found")
    if f.closed_at is not None:
        raise HTTPException(status_code=400, detail="Folio is closed")

    # Validate stay_id if provided
    if data.stay_id is not None and not session.get(Stay, data.stay_id):
        raise HTTPException(status_code=400, detail="Invalid stay_id")

    item = FolioItem(
        folio_id=folio_id,
        stay_id=data.stay_id,
        kind=data.kind,
        description=data.description,
        amount=float(data.amount),
        created_at=data.created_at or datetime.utcnow(),
    )

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/folio-items/{item_id}", response_model=FolioItemRead)
def update_item(
    item_id: uuid.UUID,
    data: FolioItemUpdate,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    item = session.get(FolioItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Folio item not found")

    f = session.get(Folio, item.folio_id)
    if f and f.closed_at is not None:
        raise HTTPException(status_code=400, detail="Folio is closed")

    patch = data.model_dump(exclude_unset=True)
    for k, v in patch.items():
        setattr(item, k, v)

    session.add(item)
    session.commit()
    session.refresh(item)
    return item
