from typing import Annotated, Union

from redis.asyncio import Redis
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from fast_depends import inject, Depends
from aiogram.filters import StateFilter

from app.database.core.gateway import DatabaseGateway
from app.filter.filter_message import TriggerFilter
from app.common.marker.gateway import TransactionGatewayMarker
from app.common.marker.redis import redis_marker


send_router = Router(name=__name__)


@send_router.message(F.text, TriggerFilter(), StateFilter(None))
@inject
async def send_photo(message: Message,
                     trigger: Union[str, bool],
                     gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
                     client: Annotated[Redis, Depends(redis_marker)]):

    photo_id = await client.get(trigger)
    if photo_id:
        await message.answer_photo(photo_id)
    else:
        repository = gateway.media()
        url = (await repository.get_url(trigger)).url
        image_from_url = FSInputFile(url)
        result = await message.answer_photo(image_from_url)
        await client.set(trigger, result.photo[-1].file_id)
