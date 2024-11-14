from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain import models
from src.infra.database.repositories import repository
from tests.integration.utils import (
    insert_allocation,
    insert_batch,
    insert_order_line,
)


def test_repository_can_save_a_batch(session: Session):
    batch = models.Batch('batch1', 'RUSTY-SOAPDISH', 100)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()
    query = text(
        'SELECT reference, sku, _purchased_quantity, eta FROM batches'
    )
    rows = session.execute(query)

    assert list(rows) == [('batch1', 'RUSTY-SOAPDISH', 100, None)]


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session, 'order1', 'GENERIC-SOFA', 12)
    batch1_id = insert_batch(session, 'batch1', 'GENERIC-SOFA', 100, eta=None)
    insert_batch(session, 'batch2', 'GENERIC-SOFA', 100, eta=None)

    insert_allocation(session, orderline_id, batch1_id)

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get('batch1')

    expected = models.Batch('batch1', 'GENERIC-SOFA', 100, eta=None)

    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        models.OrderLine('order1', 'GENERIC-SOFA', 12)
    }
