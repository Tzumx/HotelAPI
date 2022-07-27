from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy import MetaData, Table
from .bookings import booking
import datetime

metadata = MetaData()

# Model of payments for booking and requests
payment = Table(
    'payments',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('booking_id', ForeignKey(booking.c.id,
                                    onupdate="CASCADE", ondelete="CASCADE")),  
    Column('sum', Float, nullable=False),
    Column('date', DateTime, index=True, nullable=False, 
                                    default=datetime.datetime.now),
    Column('description', String()),
)
