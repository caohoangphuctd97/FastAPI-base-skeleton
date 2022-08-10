from sqlalchemy import MetaData as _MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import (
    Mapped, sessionmaker, declarative_base,
    declarative_mixin, declared_attr, Session
)

from app.config import DatabaseServiceConfig

config = DatabaseServiceConfig()


MetaData = _MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


BaseModel = declarative_base(metadata=MetaData)


@declarative_mixin
class BaseMixin:
    @declared_attr
    def __tablename__(cls) -> Mapped[str]:
        return cls.__name__.lower()     # type: ignore

    def apply_update(self, **kwargs: object) -> None:
        """Apply a set of changes to an instance.

        Eg:
            obj.apply_update(**patch.dict(exclude_unset=True))
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


async_engine: AsyncEngine = create_async_engine(
    config.ASYNC_DATABASE_URI,
    **config.SQLALCHEMY_ENGINE_OPTIONS,
    future=True
)

sess = sessionmaker(     # type: ignore
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    future=True,
    class_=AsyncSession,
    expire_on_commit=False,
)
