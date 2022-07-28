from sqlalchemy import Table, Column, Integer, String, Float, Boolean, text
from sqlalchemy import MetaData, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.sql import expression

metadata = MetaData()

room = Table(
    # Model of hotel rooms
    'rooms',
    metadata,
    Column('number', Integer, primary_key=True,
           autoincrement=False),  # number of the room
    Column('type_id', ForeignKey("room_types.id",
                                 onupdate="CASCADE", ondelete="SET NULL")),
    Column('floor', Integer, CheckConstraint('floor>=0'),
           nullable=False, server_default=text("0")),
    Column('housing', Integer, CheckConstraint('housing>=0'), nullable=False, server_default=text("0")),
)

room_type = Table(
    # Model of room's types
    'room_types',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('type_name', String(), nullable=False),
    Column('price', Float, CheckConstraint('price>=0'), index=True, nullable=False),
    Column('description', String()),
)

feature = Table(
    # Model for roomtype's features
    'features',
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
    Column('feature_id', ForeignKey("features.id",
                                    onupdate="CASCADE", ondelete="CASCADE")),
    UniqueConstraint('type_id', 'feature_id'),
)
