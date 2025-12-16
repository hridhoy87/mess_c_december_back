from sqlmodel import Session, select
from app.models.user_account import UserAccount
from app.core.security import verify_password

def authenticate_user(session: Session, email: str, password: str) -> UserAccount | None:
    user = session.exec(select(UserAccount).where(UserAccount.email == email)).first()
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
