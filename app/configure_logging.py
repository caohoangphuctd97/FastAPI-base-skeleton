from pydantic import BaseModel
from logging.config import dictConfig
import logging


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "__main__"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(funcName)s.py L%(lineno)d | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "__main__": {"handlers": ["default"], "level": LOG_LEVEL},
    }


def configure_logging(log_level):
    dictConfig(LogConfig(LOG_LEVEL=log_level).dict())
