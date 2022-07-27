from sqlalchemy import Column, DateTime, Integer, String, Float, Boolean
from sqlalchemy import MetaData, Table, ForeignKey
from sqlalchemy.sql import expression
from .guests import guest_table
from .rooms import room_table
import datetime

metadata = MetaData()

# Model of bookings
booking_table = Table(
    'bookings',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('room_number', ForeignKey(room_table.c.number,
                                 onupdate="CASCADE", ondelete="SET NULL")),
    Column('guest_id', ForeignKey(guest_table.c.id,
                                  onupdate="CASCADE", ondelete="SET NULL")),
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
    Column('created_at', DateTime, index=True,
           nullable=False, default=datetime.datetime.now),
    Column('updated_at', DateTime, index=True,
           nullable=False, onupdate=datetime.datetime.now),
)
