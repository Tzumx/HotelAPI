from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy import MetaData, Table, ForeignKey
from sqlalchemy.sql import expression

metadata = MetaData()

# Model of romms
room_table = Table(
    'rooms',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('number', Integer, unique=True, index=True),  # number of the room
    Column('type_id', ForeignKey("room_types.id",
                                 onupdate="CASCADE", ondelete="CASCADE")),
    Column('is_clean', Boolean(),
           server_default=expression.true(), nullable=False),
)

# Model of room's types
room_type_table = Table(
    'room_types',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String(100), nullable=False),
    Column('price', Float, index=True, nullable=False),
    Column('description', String()),
    Column('is_doublebad', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_kitchen', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_bathroom', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_conditioner', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_TV', Boolean(),
           server_default=expression.false(), nullable=False),
)
