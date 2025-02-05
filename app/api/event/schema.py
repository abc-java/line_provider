from pydantic import BaseModel, ConfigDict, Field
from app.api.event.enum import EventState
import decimal


class BaseEvent(BaseModel):
    coefficient: decimal.Decimal = Field(ge=0.01, decimal_places=2)
    deadline: int
    state: EventState


class Event(BaseEvent):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CreateEventResponse(Event):
    pass


class UpdateEventResponse(Event):
    pass


class ReadEventResponse(Event):
    pass


class CreateEventRequest(BaseEvent):
    pass


class UpdateEventRequest(BaseModel):
    coefficient: decimal.Decimal | None = Field(ge=0.01, decimal_places=2, default=None)
    deadline: int | None = None
    state: EventState | None = None
