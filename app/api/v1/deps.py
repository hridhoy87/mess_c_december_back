from fastapi import Depends, HTTPException, Request
from sqlmodel import Session, select
from app.db.database import get_session
from app.core.security import decode_token
from app.core.config import settings
from app.models.user_account import UserAccount

def get_token_from_request(request: Request) -> str | None:
    # 1) Cookie
    token = request.cookies.get(settings.JWT_COOKIE_NAME)
    if token:
        return token

    # 2) Authorization: Bearer <token>
    auth = request.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()

    return None

def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
) -> UserAccount:
    token = get_token_from_request(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = session.exec(select(UserAccount).where(UserAccount.id == user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found")

    return user
