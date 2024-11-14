import pytest

from src.data import services
from src.domain import models
from src.domain.errors import OrderLineNotFound
from tests.fake_repository import FakeRepository, FakeSession


def test_add_batch():
    repo = FakeRepository([])
    session = FakeSession()

    services.add_batch('b1', 'BLUE-PLINTH', 100, None, repo, session)

    assert repo.get(reference='b1') is not None


def test_add_batch_service_commit():
    repo = FakeRepository([])
    session = FakeSession()

    services.add_batch('batch', 'OMINOUS-MIRROR', 100, None, repo, session)

    assert session.committed is True


def test_allocate_service_commit():
    repo = FakeRepository([])
    session = FakeSession()
    services.add_batch(
        'batch', 'OMINOUS-MIRROR', 100, None, repo, FakeSession()
    )
    services.allocate('order', 'OMINOUS-MIRROR', 10, repo, session)

    assert session.committed is True


def test_returns_allocation():
    repo = FakeRepository([])

    services.add_batch(
        'batch', 'COMPLICATED-LAMP', 100, None, repo, FakeSession()
    )

    result = services.allocate(
        'order', 'COMPLICATED-LAMP', 10, repo, FakeSession()
    )

    assert result == 'batch'


def test_error_for_invalid_sku():
    repo = FakeRepository([])
    services.add_batch('batch', 'THEREALONE', 100, None, repo, FakeSession())

    with pytest.raises(
        services.InvalidSku, match='Invalid sku NOTEXISTENTSKU'
    ):
        services.allocate('order', 'NOTEXISTENTSKU', 10, repo, FakeSession())


def test_deallocate_decrements_available_quantity():
    repo = FakeRepository([])
    services.add_batch('b1', 'BLUE-PLINTH', 100, None, repo, FakeSession())
    services.allocate('o1', 'BLUE-PLINTH', 10, repo, FakeSession())
    batch = repo.get(reference='b1')

    expected_batch_available_quantity_after_allocate = 90
    expected_batch_available_quantity_after_deallocate = 100
    assert (
        batch.available_quantity
        == expected_batch_available_quantity_after_allocate
    )

    services.deallocate('o1', 'BLUE-PLINTH', 10, repo, FakeSession())
    assert (
        batch.available_quantity
        == expected_batch_available_quantity_after_deallocate
    )


def test_deallocate_decrements_correct_quantity():
    repo = FakeRepository([])
    services.add_batch('b1', 'BLUE-PLINTH', 100, None, repo, FakeSession())
    services.add_batch('b2', 'BLUE-CHAIR', 100, None, repo, FakeSession())

    services.allocate('o1', 'BLUE-PLINTH', 10, repo, FakeSession())
    services.allocate('o1', 'BLUE-CHAIR', 10, repo, FakeSession())
    batch1 = repo.get(reference='b1')
    batch2 = repo.get(reference='b2')

    expected_batches_after_allocate = 90
    expected_batch1_after_deallocate = 100

    assert batch1.available_quantity == expected_batches_after_allocate
    assert batch2.available_quantity == expected_batches_after_allocate

    services.deallocate('o1', 'BLUE-PLINTH', 10, repo, FakeSession())

    assert batch1.available_quantity == expected_batch1_after_deallocate
    assert batch2.available_quantity == expected_batches_after_allocate


def test_trying_to_deallocate_unallocated_batch():
    repo = FakeRepository([])
    services.add_batch('b1', 'BLUE-PLINTH', 100, None, repo, FakeSession())
    line = models.OrderLine('o1', 'NOTEXISTENTSKU', 10)

    with pytest.raises(
        OrderLineNotFound, match=f'Order line not found for sku {line.sku}'
    ):
        services.deallocate('o1', 'NOTEXISTENTSKU', 10, repo, FakeSession())
