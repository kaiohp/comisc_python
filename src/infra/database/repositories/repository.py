from sqlalchemy.orm.session import Session

from src.data.interfaces.repository import RepositoryInterface
from src.domain import models


class SqlAlchemyRepository(RepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def add(self, batch: models.Batch):
        self.session.add(batch)

    def get(self, reference) -> models.Batch:
        return (
            self.session.query(models.Batch)
            .filter_by(reference=reference)
            .one()
        )

    def list(self) -> list[models.Batch]:
        return self.session.query(models.Batch).all()
