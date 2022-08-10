from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, String, Table)
from sqlalchemy.sql import expression, func

from models import guests, rooms

metadata = MetaData()

# Model of bookings hotel rooms
booking = Table(
    'bookings',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('fk_room_number', ForeignKey(rooms.room.c.number,
                                        onupdate="CASCADE", ondelete="SET NULL")),
    Column('fk_guest_id', ForeignKey(guests.guest.c.id,
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
