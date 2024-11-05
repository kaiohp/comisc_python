import pytest

from src.data import services
from src.domain import models
from tests.fake_repository import FakeRepository, FakeSession


def test_returns_allocation():
    line = models.OrderLine('order', 'COMPLICATED-LAMP', 10)
    batch = models.Batch('batch', 'COMPLICATED-LAMP', 100, eta=None)
    repo = FakeRepository([batch])

    result = services.allocate(line, repo, FakeSession())

    assert result == 'batch'


def test_error_for_invalid_sku():
    line = models.OrderLine('order', 'NOTEXISTENTSKU', 10)
    batch = models.Batch('batch', 'THEREALONE', 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(
        services.InvalidSku, match='Invalid sku NOTEXISTENTSKU'
    ):
        services.allocate(line, repo, FakeRepository)


def test_commits():
    line = models.OrderLine('order', 'OMINOUS-MIRROR', 10)
    batch = models.Batch('batch', 'OMINOUS-MIRROR', 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()

    services.allocate(line, repo, session)

    assert session.committed is True
