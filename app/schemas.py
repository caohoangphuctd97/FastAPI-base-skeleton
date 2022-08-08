from pydantic import (
    BaseModel, Field, NonNegativeInt)


class SamplingConfig(BaseModel):
    rearm_time: NonNegativeInt = Field(alias="rearmTime")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        extra = 'forbid'
