from dataclasses import dataclass
from re import search
from typing import Annotated, Union

from aiogram.types import Message
from aiogram.filters import BaseFilter
from fast_depends import inject, Depends

from app.common.marker.gateway import TransactionGatewayMarker
from app.database.core.gateway import DatabaseGateway
from app.database.repr.media.media import MediaRepr


@dataclass
class TriggerFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[dict[str, str], bool]:
        return await check(message)


@inject
async def check(message: Message,
                gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)]
                ) -> Union[dict[str, str], bool]:
    media_repr: MediaRepr = gateway.media()
    triggers = await media_repr.get_all_trigger()

    if not triggers:
        return False

    for trigger_key in triggers:
        pattern = f'{trigger_key}'
        if search(pattern.capitalize(), message.text) or search(pattern.lower(), message.text):
            return {"trigger": trigger_key}

    return False
