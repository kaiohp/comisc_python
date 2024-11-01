from sqlalchemy import text

from src.domain import models
from src.infra.database.orm import start_mappers

start_mappers()


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
