from abc import ABC, abstractmethod

from src.data.interfaces.repository import RepositoryInterface


class AbstractUnitOfWork(ABC):
    batches: RepositoryInterface

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
