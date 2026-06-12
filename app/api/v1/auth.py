from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import (
    UserRegister,
    UserLogin,
    TokenResponse
)
from app.services.auth_service import (
    create_user,
    login_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(
    user: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    created_user = await create_user(
        db,
        user
    )

    return {
        "message": "User created successfully",
        "user_id": created_user.id
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    token = await login_user(
        db,
        user.email,
        user.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return token