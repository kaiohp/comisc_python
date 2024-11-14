from datetime import date

from pydantic import BaseModel


class Batch(BaseModel):
    reference: str
    sku: str
    quantity: int
    eta: date | None = None
