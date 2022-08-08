from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

from .config import BaseMixin, BaseModel


class Trigger(BaseMixin, BaseModel):    # type: ignore
    id_ = sa.Column(
        'id', pg.UUID(as_uuid=True),
        default=uuid4, nullable=False, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    type = sa.Column(
        pg.ENUM('STANDARD', 'BUILT_IN', 'CUSTOM', name='triggertype'),
        nullable=False)
    dataset_id = sa.Column(pg.UUID(as_uuid=True))
    signal_type = sa.Column(
        pg.ENUM(
            'PGN_SEGMENT', 'PGN_EVENT', 'BUILTIN_SPN_SEGMENT',
            'BUILTIN_SPN_EVENT', 'TRIP_SEGMENT', 'TRIP_EVENT',
            'GPS_LOG_EVENT', 'ENGINE_RUN_SEGMENT', 'ENGINE_RUN_EVENT',
            'FAULT_SEGMENT', 'FAULT_EVENT', 'DIGITAL_INPUT_SEGMENT',
            'DIGITAL_INPUT_EVENT', name='triggersignaltype'),
        nullable=False)
    signal_config = sa.Column(pg.JSONB, nullable=False)
    created = sa.Column(sa.DateTime, default=datetime.now, nullable=False)
    modified = sa.Column(
        sa.DateTime, default=datetime.now,
        onupdate=datetime.now, nullable=False)
