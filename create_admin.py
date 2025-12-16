import uuid
from sqlmodel import Session, select
from app.db.database import engine
from app.models.user_account import UserAccount
from app.core.security import hash_password

EMAIL = "admin@hotel.com"
PASS = "admin123"

with Session(engine) as session:
    existing = session.exec(select(UserAccount).where(UserAccount.email == EMAIL)).first()
    if existing:
        print("Admin already exists:", existing.email)
    else:
        user = UserAccount(
            id=uuid.uuid4(),
            email=EMAIL,
            password_hash=hash_password(PASS),
            role="admin",
            is_active=True,
        )
        session.add(user)
        session.commit()
        print("Created admin:", EMAIL)
