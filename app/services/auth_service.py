from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


async def create_user(
    db: AsyncSession,
    user_data: UserRegister
):
    user = User(
    username=user_data.username,
    email=user_data.email,
    hashed_password=hash_password(
        user_data.password
    ),
    role=user_data.role
)
    

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(
        
        
    db: AsyncSession,
    email: str,
    password: str
):
    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user



async def login_user(
    db: AsyncSession,
    email: str,
    password: str
):
    user = await authenticate_user(
        db,
        email,
        password
    )

    if not user:
        return None

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }