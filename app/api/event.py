from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.user import UserResponse
from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.event import (
    EventCreate,
    EventUpdate,
    EventResponse
)

from app.schemas.registration import (
    RegistrationResponse
)

from app.services.event_service import (
    create_event,
    get_events,
    get_event_by_id,
    update_event,
    delete_event
)

from app.services.registration_service import (
    register_for_event,
    get_my_registrations
)

from app.services.registration_service import (
    register_for_event,
    get_my_registrations,
    get_event_participants
)

from app.services.event_service import (
    create_event,
    get_events,
    get_event_by_id,
    update_event,
    delete_event,
    get_my_events
)

from app.core.security import (
    get_current_user,
    require_organizer
)


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post(
    "/",
    response_model=EventResponse
)
async def create_new_event(
    event: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_organizer)
):
    return await create_event(
        db,
        event,
        organizer_id=int(current_user["sub"])
    )


@router.get(
    "/",
    response_model=list[EventResponse]
)
async def list_events(
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await get_events(
        db,
        search,
        page,
        limit
    )



@router.get(
    "/my-events",
    response_model=list[EventResponse]
)
async def my_events(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await get_my_events(
        db,
        int(current_user["sub"])
    )


@router.get(
    "/my-registrations",
    response_model=list[RegistrationResponse]
)
async def my_registrations(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await get_my_registrations(
        db,
        int(current_user["sub"])
    )



@router.get(
    "/{event_id}/participants",
    response_model=list[UserResponse]
)
async def event_participants(
    event_id: int,
    db: AsyncSession = Depends(get_db)
):
    event = await get_event_by_id(
        db,
        event_id
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return await get_event_participants(
        db,
        event_id
    )


@router.get(
    "/{event_id}",
    response_model=EventResponse
)
async def get_single_event(
    event_id: int,
    db: AsyncSession = Depends(get_db)
):
    event = await get_event_by_id(
        db,
        event_id
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


@router.put(
    "/{event_id}",
    response_model=EventResponse
)
async def update_existing_event(
    event_id: int,
    event: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_event = await get_event_by_id(
        db,
        event_id
    )

    if not existing_event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if existing_event.organizer_id != int(current_user["sub"]):
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return await update_event(
        db,
        event_id,
        event
    )


@router.delete(
    "/{event_id}"
)
async def delete_existing_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_event = await get_event_by_id(
        db,
        event_id
    )

    if not existing_event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if existing_event.organizer_id != int(current_user["sub"]):
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    await delete_event(
        db,
        event_id
    )

    return {
        "message": "Event deleted successfully"
    }


@router.post(
    "/{event_id}/register",
    response_model=RegistrationResponse
)
async def register_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    event = await get_event_by_id(
        db,
        event_id
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    registration = await register_for_event(
        db,
        user_id=int(current_user["sub"]),
        event_id=event_id
    )

    if registration is None:
        raise HTTPException(
            status_code=400,
            detail="Already registered for this event"
        )

    return registration