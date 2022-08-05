from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy import MetaData, Table, ForeignKey
from sqlalchemy.sql import expression, func
from .guests import guest
from .rooms import room

metadata = MetaData()

# Model of bookings hotel rooms
booking = Table(
    'bookings',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('fk_room_number', ForeignKey(room.c.number,
                                        onupdate="CASCADE", ondelete="SET NULL")),
    Column('fk_guest_id', ForeignKey(guest.c.id,
                                     onupdate="CASCADE", ondelete="SET NULL")),
    Column('check_in', DateTime, index=True, nullable=False),
    Column('check_out', DateTime, index=True, nullable=False),
    Column('description', String()),
    Column('is_paid', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_active', Boolean(),
           server_default=expression.true(), nullable=False),
    Column('client_review', String()),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
    Column('created_at', DateTime, server_default=func.now()),
)
