import uuid
from http import HTTPStatus


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name='product'):
    return f'sku-{name}-{random_suffix()}'


def random_batch_ref(name='reference'):
    return f'batch-{name}-{random_suffix()}'


def random_order_ref(name='reference'):
    return f'order-{name}-{random_suffix()}'


def test_api_returns_allocation(add_stock, client):
    sku, othersku = random_sku(), random_sku('other')
    earlybatch = random_batch_ref('1')
    laterbatch = random_batch_ref('2')
    otherbatch = random_batch_ref('3')

    add_stock(
        [
            (laterbatch, sku, 100, '2011-01-02'),
            (earlybatch, sku, 100, '2011-01-01'),
            (otherbatch, othersku, 100, None),
        ]
    )

    data = {'order_reference': random_order_ref(), 'sku': sku, 'quantity': 3}

    response = client.post(
        '/allocate',
        json=data,
        timeout=10,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['batch_ref'] == earlybatch


def test_allocations_are_persisted(add_stock, client):
    sku = random_sku()
    batch1, batch2 = random_batch_ref('1'), random_batch_ref('2')
    order1, order2 = random_order_ref('1'), random_order_ref('2')

    add_stock(
        [(batch1, sku, 10, '2011-01-01'), (batch2, sku, 10, '2011-01-02')]
    )

    line1 = {'order_reference': order1, 'sku': sku, 'quantity': 10}
    line2 = {'order_reference': order2, 'sku': sku, 'quantity': 10}

    response = client.post('/allocate', json=line1, timeout=10)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['batch_ref'] == batch1

    response = client.post('/allocate', json=line2, timeout=10)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['batch_ref'] == batch2


def test_400_detail_for_out_of_stock(add_stock, client):
    sku, small_batch, large_order = (
        random_sku(),
        random_batch_ref(),
        random_order_ref(),
    )

    add_stock([(small_batch, sku, 10, '2011-01-01')])
    data = {'order_reference': large_order, 'sku': sku, 'quantity': 20}

    response = client.post('/allocate', json=data, timeout=10)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == f'Out of stock for sku {sku}'


def test_400_detail_for_invalid_sku(add_stock, client):
    unknown_sku, order = random_sku('unknown'), random_order_ref()

    data = {'order_reference': order, 'sku': unknown_sku, 'quantity': 20}

    response = client.post('/allocate', json=data, timeout=10)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == f'Invalid sku {unknown_sku}'
