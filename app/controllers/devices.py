import logging
from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Devices
from app.schemas import DeviceSchema


logger = logging.getLogger("__main__")


async def create_device(
        db: AsyncSession, data: DeviceSchema) -> Devices:
    """Create new device

    Args:
        db (AsyncSession): database session
        data (DeviceSchema): input device data

    Returns:
        Devices: _description_
    """
    model = Devices(**data.dict())
    db.add(model)
    await db.commit()   # type: ignore
    return model


async def get_devices(db: AsyncSession) -> List[Devices]:
    """Get devices

    Args:
        session (Session): database session

    Returns:
        List[Devices]: Devices List
    """
    stmt = select(Devices)      # type: ignore
    result = await db.execute(stmt)
    devices = result.scalars().all()
    return devices