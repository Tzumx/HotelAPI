from sqlalchemy import (CheckConstraint, Column, ForeignKey, Integer, MetaData,
                        Numeric, String, Table, UniqueConstraint, text)

metadata = MetaData()

room = Table(
    # Model of hotel rooms
    'rooms',
    metadata,
    Column('number', Integer, primary_key=True,
           autoincrement=False),  # number of the room
    Column('fk_room_types_id', ForeignKey("room_types.id",
                                          onupdate="CASCADE", ondelete="SET NULL")),
    Column('floor', Integer, CheckConstraint('floor>=0'),
           nullable=False, server_default=text("0")),
    Column('housing', Integer, CheckConstraint('housing>=0'), nullable=False,
           server_default=text("0")),
)

room_type = Table(
    # Model of room's types
    'room_types',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('type_name', String(), nullable=False),
    Column('price', Numeric, CheckConstraint(
        'price>=0'), index=True, nullable=False),
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
    Column('fk_room_type_id', ForeignKey("room_types.id",
                                         onupdate="CASCADE", ondelete="CASCADE")),
    Column('fk_feature_id', ForeignKey("features.id",
                                       onupdate="CASCADE", ondelete="CASCADE")),
    UniqueConstraint('fk_room_type_id', 'fk_feature_id'),
)
