from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """Product Model.

    A product is identified by a SKU,
    which is short for stock-keeping unit.
    """

    sku: str
