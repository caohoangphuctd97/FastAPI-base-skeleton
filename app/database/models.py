from datetime import datetime

from sqlalchemy import Column, ForeignKey, Text, DateTime, INTEGER, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql as pg

from .config import BaseMixin, BaseModel


class Customer(BaseMixin, BaseModel):    # type: ignore
    id = Column(
        'id', pg.INTEGER(),
        autoincrement=True, nullable=False, primary_key=True)
    email = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    prefix = Column(Text, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    gender = Column(
        pg.ENUM('MALE', 'FEMALE', 'NONE', name='customergender'),
        nullable=True)
    birth_date = Column(DateTime(), onupdate=datetime.now, nullable=False)
    address = Column(Text, nullable=False)
    weight = Column(INTEGER(), nullable=False)
    height = Column(INTEGER(), nullable=False)
    group = Column(INTEGER(), nullable=False)
    device_id = Column(INTEGER(), ForeignKey("devices.id"), nullable=True)
    device = relationship(
        "Devices", back_populates="customer", cascade="all,delete"
    )   # type: ignore
    created = Column(DateTime, default=datetime.now, nullable=False)
    modified = Column(
        DateTime, nullable=True)


class Devices(BaseMixin, BaseModel):    # type: ignore
    id = Column(
        'id', pg.INTEGER(),
        autoincrement=True, nullable=False, primary_key=True)
    is_active = Column(BOOLEAN, default=False, nullable=False)
    is_delete = Column(BOOLEAN, default=False, nullable=False)
    customer = relationship(
        "Customer", back_populates="device"
    )    # type: ignore
