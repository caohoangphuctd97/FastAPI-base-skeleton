from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .config import Session


async def create_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session
