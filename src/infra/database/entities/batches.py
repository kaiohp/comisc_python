from sqlalchemy import Column, Date, Integer, String, Table

from src.infra.database.metadata import metadata

batches = Table(
    'batches',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reference', String(255)),
    Column('sku', String(255)),
    Column('_purchased_quantity', Integer, nullable=False),
    Column('eta', Date, nullable=True),
)
