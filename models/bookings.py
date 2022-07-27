from sqlalchemy import Column, DateTime, Integer, String, Float, Boolean
from sqlalchemy import MetaData, Table, ForeignKey
from sqlalchemy.sql import expression
from .guests import guest
from .rooms import room
import datetime

metadata = MetaData()

# Model of bookings hotel rooms
booking = Table(
    'bookings',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('room_number', ForeignKey(room.c.number,
                                 onupdate="CASCADE", ondelete="SET NULL")),
    Column('guest_id', ForeignKey(guest.c.id,
                                  onupdate="CASCADE", ondelete="SET NULL")),
    Column('check_in', DateTime, index=True, nullable=False),
    Column('check_out', DateTime, index=True, nullable=False),
    Column('description', String()),
    Column('is_paid', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('is_active', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('client_review', String()),
    Column('updated_at', DateTime, index=True,
           nullable=False, onupdate=datetime.datetime.now),
    Column('created_at', DateTime, index=True,
           nullable=False, default=datetime.datetime.now),           
)
