from sqlalchemy import Column, ForeignKey, Integer, Table

from src.infra.database.metadata import metadata

allocations = Table(
    'allocations',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('order_line_id', Integer, ForeignKey('order_lines.id')),
    Column('batch_id', Integer, ForeignKey('batches.id')),
)
