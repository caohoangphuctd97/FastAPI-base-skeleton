from typing import Literal, Optional
from datetime import datetime, date
import re

from pydantic import (
    BaseModel, NonNegativeInt, EmailStr, validator)


class DeviceSchema(BaseModel):
    is_active: bool
    is_delete: bool

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        extra = 'forbid'


class DeviceObj(DeviceSchema):
    id : int


class CustomerSchema(BaseModel):
    email: EmailStr
    phone: str
    prefix: str
    first_name: str
    last_name: str
    gender: Literal['MALE', 'FEMALE', 'NONE']
    birth_date: date
    address: str
    weight: NonNegativeInt
    height: NonNegativeInt
    group: NonNegativeInt
    device_id: Optional[int]
    device: Optional[DeviceObj]

    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        extra = 'forbid'


class CustomerObj(CustomerSchema):
    id : int
