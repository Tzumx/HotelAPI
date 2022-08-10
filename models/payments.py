from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy import MetaData, Table
from .bookings import booking
import datetime

metadata = MetaData()

# Model of payments for booking and requests
payment = Table(
    'payments',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('fk_booking_id', ForeignKey(booking.c.id,
                                       onupdate="CASCADE", ondelete="CASCADE")),
    Column('sum', Numeric, nullable=False),
    Column('date', DateTime, nullable=False, index=True,
           default=datetime.datetime.now),
    Column('description', String()),
)
