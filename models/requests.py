from email.policy import default
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy import MetaData, Table, ForeignKey
from sqlalchemy.sql import expression
from .bookings import booking_table
import datetime

metadata = MetaData()

# Model of requests
request_table = Table(
    'requests',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('booking_id', ForeignKey(booking_table.c.id,
                                    onupdate="CASCADE", ondelete="CASCADE")),
    Column('description', String(), nullable=False),
    Column('is_closed', Boolean(),
           server_default=expression.false(), nullable=False),
    Column('close_desc', String()),
    Column('created_at', DateTime, index=True,
           nullable=False, default=datetime.datetime.now),
    Column('updated_at', DateTime, index=True,
           nullable=False, onupdate=datetime.datetime.now),
)
