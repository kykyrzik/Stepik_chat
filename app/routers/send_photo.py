from typing import Annotated, AsyncContextManager

from redis.asyncio import Redis
from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from fast_depends import inject, Depends

from app.database.repr.media.media import MediaRepr
from app.filter.filter_message import TriggerFilter
from app.common.marker.gateway import TransactionGateway
from app.common.marker.redis import redis_marker


router = Router(name=__name__)


@router.message(TriggerFilter(),
                F.content_type.in_({'text'}))
@inject
async def send_photo(message: Message,
                     trigger: str,
                     gateway: Annotated[AsyncContextManager, Depends(TransactionGateway)],
                     client: Annotated[Redis, Depends(redis_marker)]):
    photo_id = client.get(trigger)
    if photo_id:
        await message.answer_photo(reply_to_message_id=photo_id)
    else:
        repository: MediaRepr = (await gateway.__aenter__()).media()
        url = (await repository.get_url(trigger)).url
        image_from_url = FSInputFile(url)
        result = await message.answer_photo(image_from_url)
        await client.set(trigger, result.photo[-1].file_id)
