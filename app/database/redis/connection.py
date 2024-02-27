import redis.asyncio as redis


async def get_connection_pool(url) -> redis.ConnectionPool:
    return redis.ConnectionPool.from_url(url)


class GetRedisConnection:
    def __init__(self, pool):
        self.pool = pool

    async def __call__(self) -> redis.Redis:
        async with redis.Redis.from_pool(self.pool) as client:
            yield client
