import redis.asyncio as redis


def get_connection_pool(url) -> redis.ConnectionPool:
    return redis.ConnectionPool.from_url(url)
