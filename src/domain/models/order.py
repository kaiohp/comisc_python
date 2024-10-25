from dataclasses import dataclass

from src.domain.models.product import Product


@dataclass(frozen=True)
class OrderLine:
    """Customers place orders.

    An order is identified by a order reference
    and comprises multiple order lines.
    each line has SKU and quantity.
    """

    reference: str
    product: Product
    quantity: int
