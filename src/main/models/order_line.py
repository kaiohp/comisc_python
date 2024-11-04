from pydantic import BaseModel


class OrderLine(BaseModel):
    order_reference: str
    sku: str
    quantity: int
