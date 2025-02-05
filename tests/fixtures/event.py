import pytest
from app.models import Event
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.db import AsyncIterator
from faker import Faker
from datetime import datetime, timezone
from app.api.event.enum import EventState

faker = Faker()


@pytest.fixture
async def event1_fixture(db: AsyncIterator[async_sessionmaker]) -> Event:
    event = Event(
        coefficient=faker.pydecimal(left_digits=3, right_digits=2, positive=True),
        deadline=(datetime.now(timezone.utc) + faker.random_int()).timestamp(),
        state=EventState.NEW,
    )
    db.add(event)
    await db.commit()

    return event


@pytest.fixture
async def event2_fixture(db: AsyncIterator[async_sessionmaker]) -> Event:
    event = Event(
        coefficient=faker.pydecimal(left_digits=3, right_digits=2, positive=True),
        deadline=(datetime.now(timezone.utc) - faker.random_int()).timestamp(),
        state=EventState.FINISHED_LOSE,
    )
    db.add(event)
    await db.commit()

    return event


@pytest.fixture
async def get_events_response_fixture():
    return {
        "items": [
            {"coefficient": "0.01", "deadline": 0, "state": 1, "id": 4},
            {"coefficient": "0.01", "deadline": 0, "state": 1, "id": 5},
        ],
        "total": 2,
        "page": 1,
        "size": 50,
        "pages": 1,
    }
