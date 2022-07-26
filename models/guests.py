from sqlalchemy import Column, Integer, String
from sqlalchemy import MetaData, Table

metadata = MetaData()

# Model of guests
guest_table = Table(
    'guests',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(), nullable=False),
    Column('email', String()),
    Column('phone', String()),
)
