from fastapi import APIRouter
from sqlmodel import text
from app.db.database import engine

router = APIRouter(tags=["dashboard"])

@router.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"ok": True}
