from sqlalchemy import Column, Integer, MetaData, String, Table

metadata = MetaData()

# Model of hotel guests
guest = Table(
    'guests',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(), nullable=False),
    Column('email', String()),
    Column('phone', String()),
)
