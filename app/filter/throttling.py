from time import time

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ThrottlingFilter(BaseFilter):
    def __init__(self, rate: int):
        self.throttling_rate = rate
        self.last_executed = time()

    async def __call__(self, message: Message) -> bool:
        current_time = time()
        if not self.last_executed:
            self.last_executed = current_time - self.throttling_rate - 1

        if current_time - self.last_executed > self.throttling_rate:
            self.last_executed = current_time
            return True
        else:
            return False
