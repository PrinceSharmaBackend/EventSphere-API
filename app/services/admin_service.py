from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.event import Event


async def get_all_users(
    db: AsyncSession
):
    result = await db.execute(
        select(User)
    )

    return result.scalars().all()


async def get_all_events(
    db: AsyncSession
):
    result = await db.execute(
        select(Event)
    )

    return result.scalars().all()