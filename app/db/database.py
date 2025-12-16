from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    # Dev-only convenience. In real use, prefer alembic migrations.
    SQLModel.metadata.create_all(engine)
