import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infra.database.metadata import metadata


@pytest.fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)

    return engine


@pytest.fixture
def session(in_memory_db):
    Session = sessionmaker(in_memory_db)
    return Session()
