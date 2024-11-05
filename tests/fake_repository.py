from src.data.interfaces.repository import RepositoryInterface
from src.domain.models import Batch


class FakeRepository(RepositoryInterface):
    def __init__(self, batches: list[Batch]) -> None:
        self._batches = set(batches)

    def add(self, batch: Batch):
        self._batches.add(batch)

    def get(self, reference: str):
        return next(
            batch for batch in self._batches if batch.reference == reference
        )

    def list(self):
        return list(self._batches)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True
