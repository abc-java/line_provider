from fastapi import APIRouter, Depends
from app.api.event import service, schema
from app.db import get_session, AsyncSession
from fastapi_pagination import Page, paginate
from app.api.event.enum import EventState


router = APIRouter(prefix="/events")


@router.get("/", response_model=Page[schema.Event])
async def read_all(
    session: AsyncSession = Depends(get_session), state_filter: EventState = None
) -> Page[schema.Event]:
    return paginate(
        [event async for event in service.get_events(session, state_filter)]
    )


@router.get("/{id}", response_model=schema.ReadEventResponse)
async def read(id: int, session: AsyncSession = Depends(get_session)) -> schema.Event:
    return await service.get_event(session, id)


@router.post("/", response_model=schema.CreateEventResponse)
async def create(
    data: schema.CreateEventRequest, session: AsyncSession = Depends(get_session)
) -> schema.Event:
    return await service.create_event(
        session, data.coefficient, data.deadline, data.state
    )


@router.put("/{id}", response_model=schema.UpdateEventResponse)
async def update(
    id: int,
    data: schema.UpdateEventRequest,
    session: AsyncSession = Depends(get_session),
) -> schema.Event:
    return await service.update_event(
        session, id, data.coefficient, data.deadline, data.state
    )


@router.delete("/id}", status_code=204)
async def delete(id: int, session: AsyncSession = Depends(get_session)) -> None:
    await service.delete_event(session, id)
