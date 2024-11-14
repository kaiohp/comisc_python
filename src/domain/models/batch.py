from datetime import date
from typing import Optional

from src.domain.models.order import OrderLine


class Batch:
    """Purchasing department orders small batches of stock.

    A batch of stock has a unique ID called reference, SKU, quantity and a ETA.
    Batches have an ETA if they are currently shipping,
    or they may be in warehouse stock.

    """

    def __init__(
        self,
        reference: str,
        sku: str,
        quantity: int,
        eta: Optional[date] = None,
    ):
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = quantity
        self._allocations: set[OrderLine] = set()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False

        return self.reference == other.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other: object):
        if not isinstance(other, Batch):
            raise ValueError(
                f"'>' not supported between instances of"
                f'{self.__class__} and {other.__class__}'
            )

        if self.eta is None:
            return False

        if other.eta is None:
            return True

        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        """When we allocate x units of stock to a batch,
        the available quantity is reduced by x.
        """
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if self.can_deallocate(line):
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return (
            self.sku == line.sku and self.available_quantity >= line.quantity
        )

    def can_deallocate(self, line: OrderLine) -> bool:
        return line in self._allocations
