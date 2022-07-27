from sqlalchemy import Column, DateTime, Integer, String, Boolean, Float
from sqlalchemy import MetaData, Table, ForeignKey
from sqlalchemy.sql import expression
from .bookings import booking
import datetime

metadata = MetaData()

# Model of requests (for any services)
request = Table(
    'requests',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('booking_id', ForeignKey(booking.c.id,
                                    onupdate="CASCADE", ondelete="CASCADE")),
    Column('description', String(), nullable=False),
    Column('is_closed', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('close_description', String()),
    Column('price', Float, index=True, nullable=False),
    Column('created_at', DateTime, index=True,
           nullable=False, default=datetime.datetime.now),
    Column('updated_at', DateTime, index=True,
           nullable=False, onupdate=datetime.datetime.now),
)
