from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session

from app.db.database import get_session
from app.core.security import create_access_token
from app.core.config import settings
from app.schemas.auth import LoginRequest, LoginResponse, UserMeResponse
from app.services.auth_service import authenticate_user
from app.api.v1.deps import get_current_user

router = APIRouter(tags=["auth"])

@router.post("/auth/login", response_model=LoginResponse)
def login(data: LoginRequest, response: Response, session: Session = Depends(get_session)):
    user = authenticate_user(session, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
    })

    # Optional: backend-managed cookie (works even without Next BFF).
    # If you want BFF-only cookies, you can remove this later.
    response.set_cookie(
        key=settings.JWT_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite="lax",
        max_age=settings.JWT_EXPIRES_MINUTES * 60,
        path="/",
    )

    return LoginResponse(access_token=token)

@router.post("/auth/logout")
def logout(response: Response):
    # Clears backend cookie (harmless if you’re using BFF cookie instead)
    response.delete_cookie(key=settings.JWT_COOKIE_NAME, path="/")
    return {"ok": True}

@router.get("/auth/me", response_model=UserMeResponse)
def me(user = Depends(get_current_user)):
    return UserMeResponse(id=str(user.id), email=user.email, role=user.role)
