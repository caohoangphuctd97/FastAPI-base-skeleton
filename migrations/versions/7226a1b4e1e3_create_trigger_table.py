"""create trigger table

Revision ID: 7226a1b4e1e3
Revises:
Create Date: 2022-03-10 21:56:02.215755

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

# revision identifiers, used by Alembic.
revision = '7226a1b4e1e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'trigger',
        sa.Column('id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column(
            'type',
            pg.ENUM(
                'STANDARD', 'BUILT_IN', 'CUSTOM', name='triggertype'),
            nullable=False),
        sa.Column('dataset_id', pg.UUID(as_uuid=True), nullable=True),
        sa.Column(
            'signal_type',
            pg.ENUM(
                'PGN_SEGMENT', 'PGN_EVENT', 'BUILTIN_SPN_SEGMENT',
                'BUILTIN_SPN_EVENT', 'TRIP_SEGMENT', 'TRIP_EVENT',
                'GPS_LOG_EVENT', 'ENGINE_RUN_SEGMENT',
                'ENGINE_RUN_EVENT', 'FAULT_SEGMENT', 'FAULT_EVENT',
                'DIGITAL_INPUT_SEGMENT', 'DIGITAL_INPUT_EVENT',
                name='triggersignaltype'),
            nullable=False),
        sa.Column(
            'signal_config',
            pg.JSONB(astext_type=sa.Text()),
            nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('modified', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_trigger'))
    )


def downgrade():
    op.drop_table('trigger')
    pg.ENUM(name='triggertype').drop(op.get_bind())
    pg.ENUM(name='triggersignaltype').drop(op.get_bind())
