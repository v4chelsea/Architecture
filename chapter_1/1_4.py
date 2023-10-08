from models import *
from typing import List

def allocate(line: OrderLine, batches: List[Batch]) -> str:
    batch = next(
        b for b in sorted(batches) if b.can_allocate(line)
    )

    batch.allocate(line)
    return batch.reference


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tommorow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=tommorow)
    latest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine('order1', "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.allocated_quantity == 90
    assert medium.allocated_quantity == 100
    assert latest.allocated_quantity == 100

def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "HIGHBROW-POSTER", 100, eta=tommorow)
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference