import logging
from typing import List

from fastapi_jwt_auth import AuthJWT

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import Customer, Devices
from app.schemas import CustomerSchema, ReqLoginSchema, ResLoginSchema
from app.exceptions.configure_exceptions import (
    ItemDoesNotExist, CustomerNotFound
)

from app.utils.auth import (
    PasswordHandle, customer_claims, create_auth_tokens
)


logger = logging.getLogger("__main__")


async def create_customer(
        db: AsyncSession, data: CustomerSchema) -> Customer:
    """Create Customer from provided input data

    Args:
        db (Session): database session
        data (CustomerSchema): input customer data

    Returns:
        Customer: created customer
    """
    if data.device_id is not None:
        stmt = select(Devices).filter(Devices.id == data.device_id)
        result = await db.execute(stmt)
        if result.first() is None:
            raise ItemDoesNotExist("Device", data.device_id)
    password_handle = PasswordHandle()
    hash_password = password_handle.get_password_hash(data.password)
    data.password = hash_password
    model = Customer(**data.dict())
    db.add(model)
    await db.commit()   # type: ignore
    return model


async def get_customers(db: AsyncSession) -> List[Customer]:
    """Get customers

    Args:
        db (Session): database session

    Returns:
        List[Customer]: Customers List
    """
    stmt = select(Customer).options(selectinload(Customer.device))
    result = await db.execute(stmt)
    customers = result.scalars().all()
    return customers


async def get_customers_by_device_id(
    db: AsyncSession, device_id: int
) -> List[Customer]:
    """Get customers by device_id

    Args:
        db (Session): database session

    Returns:
        List[Customer]: Customers List
    """
    if device_id is not None:
        stmt = select(Devices).filter(Devices.id == device_id)
        result = await db.execute(stmt)
        if result.first() is None:
            raise ItemDoesNotExist("Device", device_id)
    stmt = select(Customer).options(
        selectinload(Customer.device)
    ).filter(Customer.device_id == device_id)      # type: ignore
    result = await db.execute(stmt)
    customers = result.scalars().all()
    return customers


async def login(
    db: AsyncSession, data: ReqLoginSchema, redis_db
) -> ResLoginSchema:
    """Login

    Args:
        db (AsyncSession): database session
        data (ReqLoginSchema): Login Data

    Returns:
        ResLoginSchema: Token
    """
    stmt = select(Customer).options(
        selectinload(Customer.device)
    ).filter(Customer.email == data.email)      # type: ignore
    result = await db.execute(stmt)
    customer = result.scalars().first()
    if customer is None:
        raise CustomerNotFound()
    password_handle = PasswordHandle()
    password_handle.verify_password(
        plain_password=data.password,
        hashed_password=customer.password
    )
    claims = customer_claims(
        email=data.email,
        phone=customer.phone,
        first_name=customer.first_name,
        last_name=customer.last_name,
        customer_id=customer.id
    )
    authorize = AuthJWT()
    access_token, refresh_token = create_auth_tokens(
        authorize=authorize,
        subject="customer",
        redis_db=redis_db,
        claims=claims
    )
    return ResLoginSchema(
        access_token=access_token, refresh_token=refresh_token
    )
