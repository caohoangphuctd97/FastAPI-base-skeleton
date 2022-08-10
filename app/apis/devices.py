import logging

from typing import List
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers
from app.database.depends import create_session
from app.schemas import DeviceSchema, DeviceObj

# from .custom_types import PaginationParams, PaginationResponseHeaders

logger = logging.getLogger("__main__")

router = APIRouter(
    prefix="/device",
    tags=["device"]
)

GET_DEVICE_STATUS_CODES = {
    200: {"description": "Resource found."},
    404: {"description": "Resource not found."},
}

POST_DEVICE_STATUS_CODES = {
    201: {'description': 'Resource created.'},
    400: {'description': 'Resource body failed a constraint check.'},
    409: {'description': 'Resource is a duplicate.'},
}

GET_DEVICES_STATUS_CODES = {
    200: {"description": "Search results maching criteria"},
    422: {"description": "Invalid input, params invalid."},
}

PATCH_DEVICE_STATUS_CODES = {
    204: {'description': 'Resource patched.'},
    404: {'description': 'Resource not found.'},
    409: {'description': 'Resource is a duplicate.'}
}


@router.post(
    '',
    response_model=DeviceObj,
    responses=POST_DEVICE_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def create_device(
        data: DeviceSchema,
        db: AsyncSession = Depends(create_session)):
    logger.info(f'Creating customer with data={data}')
    return await controllers.devices.create_device(db, data)


@router.get(
    '',
    response_model=List[DeviceObj],
    responses=GET_DEVICES_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_200_OK,
)
async def get_devices(
        db: AsyncSession = Depends(create_session)):
    logger.info(f'Get devices')
    return await controllers.devices.get_devices(db)
