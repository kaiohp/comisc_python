from datetime import date

from sqlalchemy import text

from src.domain import models


def test_orderline_mapper_can_load_lines(session):
    query = text(
        'INSERT INTO order_lines (order_reference, sku, quantity)'
        'VALUES'
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    )

    session.execute(query)

    expected = [
        models.OrderLine('order1', 'RED-CHAIR', 12),
        models.OrderLine('order1', 'RED-TABLE', 13),
        models.OrderLine('order2', 'BLUE-LIPSTICK', 14),
    ]

    assert session.query(models.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = models.OrderLine('order1', 'DECORATIVE-WIDGET', 12)
    session.add(new_line)
    session.commit()

    query = text('SELECT order_reference, sku, quantity FROM "order_lines"')
    rows = list(session.execute(query))
    assert rows == [
        (new_line.order_reference, new_line.sku, new_line.quantity)
    ]


def test_retrieving_batches(session):
    session.execute(
        text(
            'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
            'VALUES'
            '("batch1", "sku1", 100, null),'
            '("batch2", "sku2", 200, "2011-04-11")'
        )
    )

    expected = [
        models.Batch('batch1', 'sku1', 100, None),
        models.Batch('batch2', 'sku2', 200, eta=date(2011, 4, 11)),
    ]

    assert session.query(models.Batch).all() == expected


def test_saving_batches(session):
    batch = models.Batch('batch1', 'sku1', 100, None)
    session.add(batch)
    session.commit()
    rows = session.execute(
        text('SELECT reference, sku, _purchased_quantity, eta from batches')
    )
    assert list(rows) == [('batch1', 'sku1', 100, None)]


def test_saving_allocations(session):
    batch = models.Batch('batch1', 'DECORATIVE-WIDGET', 100, None)
    line = models.OrderLine('order1', 'DECORATIVE-WIDGET', 12)

    batch.allocate(line)

    session.add(batch)
    session.commit()

    rows = session.execute(
        text('SELECT order_line_id, batch_id FROM allocations')
    )

    assert list(rows) == [(batch.id, line.id)]


def test_retrieving_allocations(session):
    session.execute(
        text(
            'INSERT INTO order_lines (order_reference, sku, quantity)'
            'VALUES ("order1", "sku1", 10)'
        )
    )
    [[order_id]] = session.execute(
        text(
            'SELECT id FROM order_lines WHERE order_reference="order1" AND sku="sku1"'
        )
    )

    session.execute(
        text(
            'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
            'VALUES ("batch1", "sku1", 100, null)'
        )
    )
    [[batch_id]] = session.execute(
        text('SELECT id FROM batches WHERE reference="batch1" AND sku="sku1"')
    )

    session.execute(
        text(
            'INSERT INTO allocations (order_line_id, batch_id)'
            'VALUES (:order_id,:batch_id)'
        ),
        {'order_id': order_id, 'batch_id': batch_id},
    )

    batch = session.query(models.Batch).one()

    assert batch._allocations == {models.OrderLine('order1', 'sku1', 10)}
