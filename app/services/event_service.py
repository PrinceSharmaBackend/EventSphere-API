from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.event import EventCreate
from app.schemas.event import (
    EventCreate,
    EventUpdate
)


async def create_event(
    db: AsyncSession,
    event_data: EventCreate,
    organizer_id: int
):
    event = Event(
        title=event_data.title,
        description=event_data.description,
        location=event_data.location,
        event_date=event_data.event_date,
        organizer_id=organizer_id
    )

    db.add(event)

    await db.commit()
    await db.refresh(event)

    return event


async def get_events(
    db: AsyncSession,
    search: str | None = None,
    page: int = 1,
    limit: int = 10
):
    query = select(Event)

    if search:
        query = query.where(
            Event.title.ilike(f"%{search}%")
        )

    query = query.offset(
        (page - 1) * limit
    ).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()

async def get_event_by_id(
    db: AsyncSession,
    event_id: int
):
    result = await db.execute(
        select(Event).where(
            Event.id == event_id
        )
    )

    return result.scalar_one_or_none()


async def update_event(
    db: AsyncSession,
    event_id: int,
    event_data: EventUpdate
):
    event = await get_event_by_id(
        db,
        event_id
    )

    if not event:
        return None

    event.title = event_data.title
    event.description = event_data.description
    event.location = event_data.location
    event.event_date = event_data.event_date

    await db.commit()
    await db.refresh(event)

    return event

async def delete_event(
    db: AsyncSession,
    event_id: int
):
    event = await get_event_by_id(
        db,
        event_id
    )

    if not event:
        return False

    await db.delete(event)
    await db.commit()

    return True

async def get_my_events(
    db: AsyncSession,
    organizer_id: int
):
    result = await db.execute(
        select(Event).where(
            Event.organizer_id == organizer_id
        )
    )

    return result.scalars().all()