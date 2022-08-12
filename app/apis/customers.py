import logging

from redis import Redis
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers
from app.database.depends import create_session
from app.schemas import (
        CustomerSchema, CustomerObj, ReqLoginSchema, ResLoginSchema,
        ResCreateCustomer
    )
from app.utils.get_db import get_redis_db
from app.utils.auth import depend_customer_access_token
# from .custom_types import PaginationParams, PaginationResponseHeaders

logger = logging.getLogger("__main__")

router = APIRouter(
    prefix="/customer",
    tags=["customer"]
)

GET_CUSTOMER_STATUS_CODES = {
    200: {"description": "Resource found."},
    404: {"description": "Resource not found."},
}

POST_CUSTOMER_STATUS_CODES = {
    201: {'description': 'Resource created.'},
    400: {'description': 'Resource body failed a constraint check.'},
    409: {'description': 'Resource is a duplicate.'},
}

GET_CUSTOMERS_STATUS_CODES = {
    200: {"description": "Search results maching criteria"},
    422: {"description": "Invalid input, params invalid."},
}

PATCH_CUSTOMER_STATUS_CODES = {
    204: {'description': 'Resource patched.'},
    404: {'description': 'Resource not found.'},
    409: {'description': 'Resource is a duplicate.'}
}


@router.post(
    '',
    response_model=ResCreateCustomer,
    responses=POST_CUSTOMER_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
        data: CustomerSchema,
        db: AsyncSession = Depends(create_session)):
    logger.info(f'Creating customer with data={data}')
    return await controllers.customers.create_customer(db, data)


@router.post(
    '/login',
    response_model=ResLoginSchema,
    responses=POST_CUSTOMER_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_200_OK,
)
async def login(
        data: ReqLoginSchema,
        db: AsyncSession = Depends(create_session),
        redis_db: Redis = Depends(get_redis_db)):
    return await controllers.customers.login(db, data, redis_db)


@router.get(
    '',
    response_model=List[CustomerObj],
    responses=GET_CUSTOMERS_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_200_OK,
)
async def get_customers(
    authorize: AuthJWT = Depends(depend_customer_access_token),
    db: AsyncSession = Depends(create_session)
):
    logger.info('Get customers')
    return await controllers.customers.get_customers(db)


@router.get(
    '/device/{device_id}',
    response_model=List[CustomerObj],
    responses=GET_CUSTOMERS_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_200_OK,
)
async def get_customer_by_device_id(
        device_id: int,
        db: AsyncSession = Depends(create_session)):
    logger.info('Get customers')
    return await controllers.customers.get_customers_by_device_id(db, device_id)    # noqa: E501
