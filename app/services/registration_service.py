from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.registration import Registration


async def register_for_event(
    db: AsyncSession,
    user_id: int,
    event_id: int
):
    existing_registration = await db.execute(
        select(Registration).where(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        )
    )

    if existing_registration.scalar_one_or_none():
        return None

    registration = Registration(
        user_id=user_id,
        event_id=event_id
    )

    db.add(registration)

    await db.commit()
    await db.refresh(registration)

    return registration

from sqlalchemy import select


async def get_my_registrations(
    db: AsyncSession,
    user_id: int
):
    result = await db.execute(
        select(Registration).where(
            Registration.user_id == user_id
        )
    )

    return result.scalars().all()

from app.models.user import User


async def get_event_participants(
    db: AsyncSession,
    event_id: int
):
    result = await db.execute(
        select(User)
        .join(
            Registration,
            User.id == Registration.user_id
        )
        .where(
            Registration.event_id == event_id
        )
    )

    return result.scalars().all()