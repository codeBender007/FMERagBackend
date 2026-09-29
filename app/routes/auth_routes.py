# app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.connection import get_db
from core.security import verify_password, create_access_token
from schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    query = text("""
        SELECT TOP 1 id, fullName, userName, password, role 
        FROM users 
        WHERE userName = :u AND isDeleted = 0
    """)
    user = db.execute(query, {"u": payload.username}).mappings().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Legacy plain text ya Bcrypt hash dono support karta hai
    is_valid = False
    try:
        is_valid = verify_password(payload.password, user["password"])
    except Exception:
        is_valid = (payload.password == user["password"])

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(data={"sub": str(user["id"]), "role": user["role"]})
    return TokenResponse(
        access_token=token,
        user_id=user["id"],
        full_name=user["fullName"],
        role=user["role"]
    )