from src.domain import models
from tests.integration.utils import get_allocated_batch_ref, insert_batch


def test_uow_can_retrieve_a_batch_and_allocate_to_it(session_factory):
    session = session_factory()
    insert_batch(session, 'batch1', 'HIPSTER-WORKBENCH', 100, eta=None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)

    with uow:
        batch = uow.batches.get(reference='batch1')
        line = models.OrderLine('o1', 'HIPSTER-WORKBENCH', 10)
        batch.allocate(line)
        uow.commit()

    batchref = get_allocated_batch_ref(session, 'o1', 'HIPSTER-WORKBENCH')
    assert batchref == 'batch1'
