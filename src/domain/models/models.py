class Product:
    def __init__(self, SKU) -> None:
        self.SKU = SKU


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        self.product = product
        self.quantity = quantity


class Order:
    def __init__(self, order_reference, order_lines) -> None:
        self.order_reference = order_reference
        self.order_lines = order_lines
