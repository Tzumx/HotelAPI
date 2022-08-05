from sqlalchemy import Column, DateTime, Integer, String, Boolean, Numeric
from sqlalchemy import MetaData, Table, ForeignKey
from sqlalchemy.sql import expression, func
from .bookings import booking
import datetime

metadata = MetaData()

# Model of requests (for any services)
request = Table(
    'requests',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('fk_booking_id', ForeignKey(booking.c.id,
                                       onupdate="CASCADE", ondelete="CASCADE")),
    Column('description', String(), nullable=False),
    Column('is_closed', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('close_description', String()),
    Column('price', Numeric, nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
    Column('created_at', DateTime, server_default=func.now()),
)
