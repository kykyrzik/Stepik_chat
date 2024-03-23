from typing import Annotated

from redis.asyncio import Redis
from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from fast_depends import inject, Depends
from aiogram.filters import StateFilter

from app.database.core.gateway import DatabaseGateway
from app.filter.filter_message import TriggerFilter
from app.common.marker.gateway import TransactionGatewayMarker
from app.common.marker.redis import redis_marker


router = Router(name=__name__)


@router.message(TriggerFilter(), StateFilter(None))
@inject
async def send_photo(message: Message,
                     trigger: str,
                     gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
                     client: Annotated[Redis, Depends(redis_marker)]):
    print("send")
    photo_id = await client.get(trigger)
    if photo_id:
        await message.answer_photo(reply_to_message_id=photo_id)
    else:
        repository = gateway.media()
        url = (await repository.get_url(trigger)).url
        image_from_url = FSInputFile(url)
        result = await message.answer_photo(image_from_url)
        await client.set(trigger, result.photo[-1].file_id)
