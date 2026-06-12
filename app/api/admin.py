from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_admin

from app.schemas.user import UserResponse
from app.schemas.event import EventResponse

from app.services.admin_service import (
    get_all_users,
    get_all_events
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get(
    "/users",
    response_model=list[UserResponse]
)
async def admin_get_users(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin)
):
    return await get_all_users(db)


@router.get(
    "/events",
    response_model=list[EventResponse]
)
async def admin_get_events(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin)
):
    return await get_all_events(db)