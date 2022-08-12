import redis
from app.config import config


pool = redis.ConnectionPool(
    host=config.redis.redis_host,
    port=config.redis.redis_port
)

RedisSession = redis.Redis(connection_pool=pool)
