import logging
from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import Customer, Devices
from app.schemas import CustomerSchema
from app.exceptions.configure_exceptions import ItemDoesNotExist


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
    model = Customer(**data.dict())
    db.add(model)
    await db.commit()   # type: ignore
    return model


async def get_customers(db: AsyncSession) -> List[Customer]:
    """Get customers

    Args:
        session (Session): database session

    Returns:
        List[Customer]: Customers List
    """
    stmt = select(Customer).options(selectinload(Customer.device))      # type: ignore
    result = await db.execute(stmt)
    customers = result.scalars().all()
    return customers


async def get_customers_by_device_id(db: AsyncSession, device_id) -> List[Customer]:
    """Get customers

    Args:
        session (Session): database session

    Returns:
        List[Customer]: Customers List
    """
    if device_id is not None:
        stmt = select(Devices).filter(Devices.id == device_id)
        result = await db.execute(stmt)
        if result.first() is None:
            raise ItemDoesNotExist("Device", device_id)
    stmt = select(Customer).options(selectinload(Customer.device)).filter(Customer.device_id == device_id)      # type: ignore
    result = await db.execute(stmt)
    customers = result.scalars().all()
    return customers
