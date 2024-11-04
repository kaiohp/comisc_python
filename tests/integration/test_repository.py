from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain import models
from src.infra.database.repositories import repository


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


def insert_order_line(session):
    insert_query = text(
        'INSERT INTO order_lines (order_reference, sku, quantity)'
        'VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    session.execute(insert_query)

    select_query = text(
        'SELECT id FROM order_lines WHERE order_reference=:order_reference AND sku=:sku'
    )
    [[order_line_id]] = session.execute(
        select_query,
        dict(order_reference='order1', sku='GENERIC-SOFA'),
    )
    return order_line_id


def insert_batch(session, batch_id):
    insert_query = text(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
        'VALUES (:reference, "GENERIC-SOFA", 100, null)'
    )
    session.execute(insert_query, dict(reference=batch_id))

    select_query = text(
        'SELECT id FROM batches WHERE reference=:reference AND sku="GENERIC-SOFA"'
    )
    [[order_line_id]] = session.execute(
        select_query,
        dict(reference=batch_id),
    )
    return order_line_id


def insert_allocation(session, order_line_id, batch_id):
    query = text(
        'INSERT INTO allocations (order_line_id, batch_id)'
        'VALUES (:order_line_id, :batch_id)'
    )
    session.execute(
        query,
        dict(order_line_id=order_line_id, batch_id=batch_id),
    )


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, 'batch1')
    insert_batch(session, 'batch2')

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
