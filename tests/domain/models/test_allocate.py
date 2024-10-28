from datetime import date, timedelta

import pytest

from src.domain.errors import OutOfStock
from src.domain.models import Batch, OrderLine, Product, allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    product = Product('RETRO-CLOCK')
    in_stock_batch = Batch('in-stock-batch', product, 100, eta=None)
    shipment_batch = Batch('shipment-batch', product, 100, eta=tomorrow)
    line = OrderLine('order-reference', product, 10)

    allocate(line, [in_stock_batch, shipment_batch])

    expected_in_stock_batch_available_quantity = 100 - 10
    expected_shipment_batch_available_quantity = 100

    assert (
        in_stock_batch.available_quantity
        == expected_in_stock_batch_available_quantity
    )
    assert (
        shipment_batch.available_quantity
        == expected_shipment_batch_available_quantity
    )


def test_prefers_earlier_batches():
    product = Product('MINIMALIST-SPOON')
    earliest = Batch('speedy-batch', product, 100, eta=today)
    medium = Batch('normal-batch', product, 100, eta=tomorrow)
    latest = Batch('slow-batch', product, 100, eta=later)
    line = OrderLine('order-reference', product, 10)

    allocate(line, [medium, earliest, latest])

    expected_earliest_batch_available_quantity = 100 - 10
    expected_medium_batch_available_quantity = 100
    expected_latest_batch_available_quantity = 100

    assert (
        earliest.available_quantity
        == expected_earliest_batch_available_quantity
    )
    assert (
        medium.available_quantity == expected_medium_batch_available_quantity
    )
    assert (
        latest.available_quantity == expected_latest_batch_available_quantity
    )


def test_returns_allocated_batch_ref():
    product = Product('HIGHBROW-POSTER')
    in_stock_batch = Batch('in-stock-batch-ref', product, 100, eta=None)
    shipment_batch = Batch('shipment-batch-ref', product, 100, eta=tomorrow)
    line = OrderLine('order-reference', product, 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    product = Product('SMALL-FORK')
    batch = Batch('batch1', product, 10, eta=today)
    allocate(OrderLine('order1', product, 10), [batch])

    with pytest.raises(OutOfStock, match=product.sku):
        allocate(OrderLine('order2', product, 1), [batch])
