import logging

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers
from app.database.depends import create_session
from app.schemas import SamplingConfig

# from .custom_types import PaginationParams, PaginationResponseHeaders

logger = logging.getLogger("__main__")

router = APIRouter(
    prefix="/saansook",
    tags=["saansook"]
)

GET_SAANSOOK_STATUS_CODES = {
    200: {"description": "Resource found."},
    404: {"description": "Resource not found."},
}

POST_SAANSOOK_STATUS_CODES = {
    201: {'description': 'Resource created.'},
    400: {'description': 'Resource body failed a constraint check.'},
    409: {'description': 'Resource is a duplicate.'},
}

GET_SAANSOOKS_STATUS_CODES = {
    200: {"description": "Search results maching criteria"},
    422: {"description": "Invalid input, params invalid."},
}

PATCH_SAANSOOK_STATUS_CODES = {
    204: {'description': 'Resource patched.'},
    404: {'description': 'Resource not found.'},
    409: {'description': 'Resource is a duplicate.'}
}


@router.post(
    '',
    response_model=SamplingConfig,
    responses=POST_SAANSOOK_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def create_data(
        data: SamplingConfig,
        session: AsyncSession = Depends(create_session)):
    logger.info(f'Creating with data={data}')
    return await controllers.saansook.create_trigger(session, data)
