from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import logging

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

logger = logging.getLogger("__main__")


@router.get("", response_class=PlainTextResponse)
async def healthcheck():
    logger.info("Health Check")
    return PlainTextResponse(content="Ok", status_code=200)
