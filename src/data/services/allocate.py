from src.data.interfaces.repository import RepositoryInterface
from src.domain import models
from src.domain.models.batch import Batch
from src.domain.models.order import OrderLine


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches: list[Batch]):
    return any(batch.sku == sku for batch in batches)


def allocate(
    order_reference: str,
    sku: str,
    quantity: int,
    repo: RepositoryInterface,
    session,
) -> str:
    batches = repo.list()
    line = OrderLine(order_reference, sku, quantity)

    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')

    batch_ref = models.allocate(line, batches)
    session.commit()

    return batch_ref
