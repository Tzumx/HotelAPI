from sqlalchemy import Column, DateTime, Integer, String, Float, Boolean
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


# Model of guests
guest = Table(
    'guests',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(), nullable=False),
    Column('email', String()),
    Column('phone', String()),
)

# Model of bookings
booking = Table(
    'bookings',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('room_id', ForeignKey("rooms.id",
                                 onupdate="CASCADE", ondelete="CASCADE")),
    Column('guest_id', ForeignKey("guests.id",
                                  onupdate="CASCADE", ondelete="CASCADE")),
    Column('check_in', DateTime, index=True, nullable=False),
    Column('check_out', DateTime, index=True, nullable=False),
    Column('description', String()),
    Column('is_paid', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_kitchen', Boolean(),
           server_default=expression.false(),
           nullable=False),
    Column('is_check_in', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_check_out', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_active', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_need_food', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('total_price', Float, index=True, nullable=False),
    Column('client_review', String()),
    Column('updated_at', DateTime, index=True, nullable=False),
)

# Model of requests
guest = Table(
    'request',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('booking_id', ForeignKey("bookings.id",
                                  onupdate="CASCADE", ondelete="CASCADE")),    
    Column('description', String(), nullable=False),
    Column('is_closed', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('close_desc', String()),
    Column('created_at', DateTime, index=True, nullable=False),
    Column('updated_at', DateTime, index=True, nullable=False),
)
