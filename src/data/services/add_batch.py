from datetime import date

from src.data.interfaces.repository import RepositoryInterface
from src.domain.models.batch import Batch


def add_batch(  # noqa: PLR0913
    reference: str,
    sku: str,
    quantity: int,
    eta: date | None,
    repo: RepositoryInterface,
    session,
):
    batch = Batch(reference, sku, quantity, eta)
    repo.add(batch)
    session.commit()
