import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_session
from app.api.v1.deps import get_current_user
from app.models.user_account import UserAccount

from app.schemas.user_account import UserAccountRead, UserAccountUpdate

router = APIRouter(tags=["users"])

def require_admin(user=Depends(get_current_user)):
    if getattr(user, "role", "") != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    return user

@router.get("/users", response_model=list[UserAccountRead])
def list_users(
    session: Session = Depends(get_session),
    _admin = Depends(require_admin),
):
    return session.exec(select(UserAccount)).all()

@router.put("/users/{user_id}", response_model=UserAccountRead)
def update_user(
    user_id: uuid.UUID,
    data: UserAccountUpdate,
    session: Session = Depends(get_session),
    _admin = Depends(require_admin),
):
    u = session.get(UserAccount, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(u, k, v)

    session.add(u)
    session.commit()
    session.refresh(u)
    return u
