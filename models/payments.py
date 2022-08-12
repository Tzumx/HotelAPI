import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, MetaData,
                        Numeric, String, Table)

from models import bookings

metadata = MetaData()

# Model of payments for booking and requests
payment = Table(
    'payments',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('fk_booking_id', ForeignKey(bookings.booking.c.id,
                                       onupdate="CASCADE", ondelete="CASCADE")),
    Column('sum', Numeric, nullable=False),
    Column('date', DateTime, nullable=False, index=True,
           default=datetime.datetime.now),
    Column('description', String()),
)
