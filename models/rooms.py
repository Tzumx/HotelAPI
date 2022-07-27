from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy import MetaData, Table, ForeignKey, UniqueConstraint
from sqlalchemy.sql import expression

metadata = MetaData()

room_table = Table(
    # Model of rooms
    'rooms',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('number', Integer, unique=True, index=True),  # number of the room
    Column('type_id', ForeignKey("room_types.id",
                                 onupdate="CASCADE", ondelete="SET NULL")),
    Column('is_clean', Boolean(),
           server_default=expression.true(), nullable=False),
)

room_type_table = Table(
    # Model of room's types
    'room_types',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('type_name', String(), nullable=False),
    Column('price', Float, index=True, nullable=False),
    Column('description', String()),
)

room_feature = Table(
    # Model for roomtype's features
    'room_features',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('feature', String(), nullable=False),
)

roomtype_feature = Table(
    # Many-to-many between roomtype and feature
    'roomtypes_features',
    metadata,
    Column('type_id', ForeignKey("room_types.id",
                                 onupdate="CASCADE", ondelete="CASCADE")),
    Column('feature_id', ForeignKey("room_features.id",
                                    onupdate="CASCADE", ondelete="CASCADE")),
    UniqueConstraint('type_id', 'feature_id'),
)
