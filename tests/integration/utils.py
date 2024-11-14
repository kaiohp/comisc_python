from sqlalchemy import text


def insert_order_line(session, order_reference, sku, quantity):
    session.execute(
        text(
            'INSERT INTO order_lines (order_reference, sku, quantity)'
            'VALUES (:order_reference, :sku, :quantity)'
        ),
        {'order_reference': order_reference, 'sku': sku, 'quantity': quantity},
    )

    [[order_line_id]] = session.execute(
        text(
            'SELECT id FROM order_lines'
            ' WHERE order_reference=:order_reference AND sku=:sku'
        ),
        {'order_reference': order_reference, 'sku': sku},
    )
    return order_line_id


def insert_batch(session, reference, sku, quantity, eta):
    session.execute(
        text(
            'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
            'VALUES (:reference, :sku, :quantity, :eta)'
        ),
        {'reference': reference, 'sku': sku, 'quantity': quantity, 'eta': eta},
    )

    [[batch_id]] = session.execute(
        text('SELECT id FROM batches WHERE reference=:reference AND sku=:sku'),
        {'reference': reference, 'sku': sku},
    )
    return batch_id


def insert_allocation(session, order_line_id, batch_id):
    session.execute(
        text(
            'INSERT INTO allocations (order_line_id, batch_id)'
            'VALUES (:order_line_id, :batch_id)'
        ),
        {'order_line_id': order_line_id, 'batch_id': batch_id},
    )


def get_allocated_batch_ref(session, order_reference, sku):
    [[order_line_id]] = session.execute(
        text(
            'SELECT id FROM order_lines'
            ' WHERE order_reference=:order_reference AND sku=:sku'
        ),
        {'order_reference': order_reference, 'sku': sku},
    )

    [[batch_ref]] = session.execute(
        text(
            'SELECT b.reference FROM allocations '
            ' JOIN batches AS b ON batch_id = b.id'
            ' WHERE order_line_id =:order_line_id'
        ),
        {'order_line_id': order_line_id},
    )

    return batch_ref
