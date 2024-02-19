import redis.asyncio as redis


async def get_connection_pool(url) -> redis.ConnectionPool:
    return redis.ConnectionPool.from_url(url)


async def get_redis_connection(pool: redis.ConnectionPool) -> redis.Redis:
    async with redis.Redis.from_pool(pool) as client:
        yield client
