from sqlalchemy.orm import registry, relationship

from src.domain import models
from src.infra.database.entities import (
    allocations_table,
    batches_table,
    order_lines_table,
    products_table,
)


def start_mappers():
    mapper_registry = registry()
    mapper_registry.map_imperatively(models.Product, products_table)
    order_lines_mapper = mapper_registry.map_imperatively(
        models.OrderLine, order_lines_table
    )
    mapper_registry.map_imperatively(
        models.Batch,
        batches_table,
        properties={
            '_allocations': relationship(
                order_lines_mapper,
                secondary=allocations_table,
                collection_class=set,
            )
        },
    )
