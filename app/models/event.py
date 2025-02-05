from __future__ import annotations

from typing import AsyncIterator
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from typing_extensions import Annotated
from app.api.event.enum import EventState
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    coefficient: Mapped[Annotated[Decimal, 2]]
    deadline: Mapped[int]
    state: Mapped[EventState]

    @classmethod
    async def read_by_id(cls, session: AsyncSession, event_id: int) -> Event | None:
        stmt = select(cls).where(cls.id == event_id)
        return await session.scalar(stmt)

    @classmethod
    async def read_all(
        cls, session: AsyncSession, state_filter=None
    ) -> AsyncIterator[Event]:
        stmt = select(cls)
        if state_filter:
            stmt = stmt.where(cls.state == state_filter)

        stream = await session.stream_scalars(stmt)
        async for row in stream:
            yield row

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        coefficient: Decimal,
        deadline: int,
        state: EventState,
    ) -> Event:
        event = Event(coefficient=coefficient, deadline=deadline, state=state)
        session.add(event)
        await session.flush()
        return event

    async def update(self, session: AsyncSession, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)
        await session.flush()

    @classmethod
    async def delete(cls, session: AsyncSession, event: Event) -> None:
        await session.delete(event)
        await session.flush()
