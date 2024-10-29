from sqlalchemy import Column, Integer, String, Table

from src.infra.database.metadata import metadata

products = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
)
