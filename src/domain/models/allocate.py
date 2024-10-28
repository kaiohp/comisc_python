from src.domain.errors.out_of_stock import OutOfStock
from src.domain.models.batch import Batch
from src.domain.models.order import OrderLine


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(line)
        )
        batch.allocate(line)
        return batch.reference
    except StopIteration as execption:
        raise OutOfStock(
            f'Out of stock for sku {line.product.sku}'
        ) from execption
