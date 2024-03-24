from dataclasses import dataclass
from re import search
from typing import Annotated

from aiogram.types import Message
from aiogram.filters import BaseFilter
from fast_depends import inject, Depends

from app.common.marker.gateway import TransactionGatewayMarker
from app.database.core.gateway import DatabaseGateway


@dataclass
class TriggerFilter(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, str]:
        return await check(message)


@inject
async def check(message: Message,
                gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)]
                ) -> dict[str, str]:
    media_repr = gateway.media()
    trigger = await media_repr.get_all_trigger()
    print(trigger)
    if trigger:
        for trigger_key in trigger:
            pattern = f'{trigger_key}'
            if search(pattern, message.text):
                return {"trigger": trigger_key}
