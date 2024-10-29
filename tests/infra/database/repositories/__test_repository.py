from src.domain import models


def test_repository_can_save_a_batch(session):
    product = models.Product('RUSTY-SOAPDISH')
    batch = models.Batch('batch1', product, 100)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    )

    assert list(rows) == [batch]


def insert_order_line(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, quantity)"
        'VALUES ("order1", "GENERIC-SOFA", 12)'
    )

    [[order_line_id]] = session.execute(
        "SELECT id FROM order_lines WHERE orderid =:orderid AND sky=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA")
    )
    return order_line_id

def insert_batch(session, batch_id):
    ...

def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")

    insert_allocation(session, orderline_id, batch1_id)

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = models.Batch("batch1", "GENERIC-SOFA", 100, eta=None)

    assert retrieved == expected
    assert retrieved.sku = expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        models.OrderLine("order1", "GENERIC-SOFA", 12)
    }
