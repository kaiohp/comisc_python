import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import clear_mappers, sessionmaker

from src.infra.database import orm
from src.infra.database.config import Settings
from src.infra.database.metadata import metadata


@pytest.fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    orm.start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture(scope='session')
def postgres_db():
    engine = create_engine(Settings().database_url)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    orm.start_mappers()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@pytest.fixture
def add_stock(postgres_session):
    batches_added = set()
    skus_added = set()

    def _add_stock(lines):
        for ref, sku, qty, eta in lines:
            postgres_session.execute(
                text(
                    'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
                    ' VALUES (:ref, :sku, :qty, :eta)'
                ),
                dict(ref=ref, sku=sku, qty=qty, eta=eta),
            )
            [[batch_id]] = postgres_session.execute(
                text(
                    'SELECT id FROM batches WHERE reference=:ref AND sku=:sku'
                ),
                dict(ref=ref, sku=sku),
            )
            batches_added.add(batch_id)
            skus_added.add(sku)
        postgres_session.commit()

    yield _add_stock

    for batch_id in batches_added:
        postgres_session.execute(
            text('DELETE FROM allocations WHERE batch_id=:batch_id'),
            dict(batch_id=batch_id),
        )
        postgres_session.execute(
            text('DELETE FROM batches WHERE id=:batch_id'),
            dict(batch_id=batch_id),
        )
    for sku in skus_added:
        postgres_session.execute(
            text('DELETE FROM order_lines WHERE sku=:sku'),
            dict(sku=sku),
        )
        postgres_session.commit()
