# routes_payments.py
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_session
from app.api.v1.deps import get_current_user

from app.models.folio import Folio
from app.models.payment import Payment

from app.schemas.payment import PaymentCreate, PaymentRead

router = APIRouter(tags=["payments"])


@router.get("/folios/{folio_id}/payments", response_model=list[PaymentRead])
def list_payments(
    folio_id: uuid.UUID,
    session: Session = Depends(get_session),
    _user = Depends(get_current_user),
):
    if not session.get(Folio, folio_id):
        raise HTTPException(status_code=404, detail="Folio not found")
    return session.exec(select(Payment).where(Payment.folio_id == folio_id)).all()


@router.post("/folios/{folio_id}/payments", response_model=PaymentRead)
def add_payment(
    folio_id: uuid.UUID,  # folio_id comes from URL path
    data: PaymentCreate,  # PaymentCreate NO LONGER has folio_id
    session: Session = Depends(get_session),
    user = Depends(get_current_user),
):
    f = session.get(Folio, folio_id)
    if not f:
        raise HTTPException(status_code=404, detail="Folio not found")
    if f.closed_at is not None:
        raise HTTPException(status_code=400, detail="Folio is closed")

    # user.id is used because payment.received_by_user_id is NOT NULL
    received_by_user_id = getattr(user, "id", None)
    if not received_by_user_id:
        raise HTTPException(status_code=500, detail="Current user missing id")

    p = Payment(
        folio_id=folio_id,  # From URL path
        amount=data.amount,
        method=data.method,
        reference=data.reference,
        received_by_user_id=received_by_user_id,
        received_at=data.received_at or datetime.utcnow(),
    )

    session.add(p)
    session.commit()
    session.refresh(p)
    return p