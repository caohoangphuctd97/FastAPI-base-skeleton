import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Trigger


logger = logging.getLogger("__main__")


async def create_trigger(
        session: AsyncSession, data) -> Trigger:
    """Create Trigger from provided input data

    Args:
        session (AsyncSession): asynchronous database session
        data (PostTriggerModel): input trigger data

    Returns:
        Trigger: created trigger
    """
    logger.debug(f'Creating Trigger with data={data}')
    model = Trigger(**data.dict())
    session.add(model)
    await session.commit()
    return model
