from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class OrderLine:
    """Customers place orders.

    An order is identified by a order reference
    and comprises multiple order lines.
    each line has SKU and quantity.
    """

    order_reference: str
    sku: str
    quantity: int
