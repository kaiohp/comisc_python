import pytest


@pytest.mark.usefixtures('restart_api')
def test_api_returns_allocation(add_stock):
    sku, othersku = random_sku(), random_sku('other')
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)

    add_stock(
        [
            (laterbatch, sku, 100, '2011-01-02'),
            (earlybatch, sku, 100, '2011-01-01'),
            (otherbatch, othersku, 100, None),
        ]
    )

    data = {'order_reference': random_order_ref(), 'sku': sku, 'quantity': 3}
    url = Settings().get_api_url()

    r = requests.post(f'{url}/allocate', json=data)

    assert r.status_code == 201
    assert r.json()['batchref'] == earlybatch
