from src.domain.errors import OrderLineNotFound
from src.domain.models.batch import Batch
from src.domain.models.order import OrderLine


def deallocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(
            batch for batch in sorted(batches) if batch.can_deallocate(line)
        )
        batch.deallocate(line)
        return batch.reference
    except StopIteration as err:
        raise OrderLineNotFound(
            f'Order line not found for sku {line.sku}'
        ) from err
