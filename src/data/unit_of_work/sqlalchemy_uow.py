from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data.interfaces.unit_of_work import AbstractUnitOfWork
from src.infra.database.config import Settings
from src.infra.database.repositories import repository

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(Settings().database_url)
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.batches = repository.SqlAlchemyRepository(self.session)
        return self

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
