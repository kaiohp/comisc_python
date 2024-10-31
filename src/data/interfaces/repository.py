from abc import ABC, abstractmethod

from src.domain import models


class RepositoryInterface(ABC):
    @abstractmethod
    def add(self, batch: models.Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> models.Batch:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[models.Batch]:
        raise NotImplementedError
