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
