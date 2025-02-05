from app.settings import settings
from app.api.event.enum import EventState
import aiohttp


async def update_bet_status(event_id: int, state: EventState) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"{settings.BET_MAKER_URL}/api/bets/update-state-from-event/{event_id}",
            params={"state": state.value},
        ) as resp:
            pass
