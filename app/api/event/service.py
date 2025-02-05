from app.api.event import schema
from app.db import AsyncSession
from app.models import Event
from fastapi import HTTPException
from typing import AsyncIterator
from app.api.event.enum import EventState
from app.api.bet_maker_client import update_bet_status
import decimal


async def get_events(
    session: AsyncSession, state_filter=None
) -> AsyncIterator[schema.Event]:
    async with session() as session:
        async for event in Event.read_all(session, state_filter):
            yield schema.Event.model_validate(event)


async def get_event(session: AsyncSession, id: int) -> schema.Event:
    async with session() as session:
        event = await Event.read_by_id(session, id)
        if not event:
            raise HTTPException(status_code=404)
        return schema.Event.model_validate(event)


async def create_event(
    session: AsyncSession,
    coefficient: decimal.Decimal,
    deadline: int,
    state: EventState,
) -> schema.Event:
    async with session.begin() as session:
        event = await Event.create(session, coefficient, deadline, state)
        return schema.Event.model_validate(event)


async def update_event(
    session: AsyncSession,
    id: int,
    coefficient: decimal.Decimal = None,
    deadline: int = None,
    state: EventState = None,
) -> schema.Event:
    async with session.begin() as session:
        event = await Event.read_by_id(session, id)
        if not event:
            raise HTTPException(status_code=404)

        if state != None and state != event.state:
            await update_bet_status(id, state)

        await event.update(
            session, coefficient=coefficient, deadline=deadline, state=state
        )
        await session.refresh(event)
        return schema.Event.model_validate(event)


async def delete_event(session: AsyncSession, id: int) -> None:
    async with session.begin() as session:
        event = await Event.read_by_id(session, id)
        if not event:
            return
        await Event.delete(session, event)
