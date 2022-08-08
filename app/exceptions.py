import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


logger = logging.getLogger("__main__")


def configure_exceptions_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def handle_orjson_exception(
        request: Request, exc: Exception
    ) -> ORJSONResponse:
        logger.error(exc, exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "content": exc.__str__()
            }
        )
