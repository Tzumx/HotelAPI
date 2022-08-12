from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, Numeric, String, Table)
from sqlalchemy.sql import expression, func

from models import bookings

metadata = MetaData()

# Model of requests (for any services)
request = Table(
    'requests',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('fk_booking_id', ForeignKey(bookings.booking.c.id,
                                       onupdate="CASCADE", ondelete="CASCADE")),
    Column('description', String(), nullable=False),
    Column('is_closed', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('close_description', String()),
    Column('price', Numeric, nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
    Column('created_at', DateTime, server_default=func.now()),
)
