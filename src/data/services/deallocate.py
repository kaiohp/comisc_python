from src.data.interfaces.repository import RepositoryInterface
from src.domain import models


def deallocate(
    order_reference: str,
    sku: str,
    quantity: int,
    repo: RepositoryInterface,
    session,
) -> str:
    batches = repo.list()
    line = models.OrderLine(order_reference, sku, quantity)
    batch_ref = models.deallocate(line, batches)
    session.commit()

    return batch_ref
