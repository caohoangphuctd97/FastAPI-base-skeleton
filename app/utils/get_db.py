import logging

from app.exceptions.configure_exceptions import ServerErrorException
from .redis import RedisSession
from redis import Redis

logger = logging.getLogger(__name__)


def get_redis_db() -> Redis:
    try:
        db = RedisSession
        logger.debug("Start db session {}".format(RedisSession))
        return db
    except Exception as e:
        logger.error(e)
        raise ServerErrorException()
