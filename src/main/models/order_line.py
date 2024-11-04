from pydantic import BaseModel


class OrderLine(BaseModel):
    order_reference: int
    sku: str
    quantity: int
