from fastapi import APIRouter, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data import services
from src.infra.database.config import Settings
from src.infra.database.repositories.repository import SqlAlchemyRepository
from src.main.models.batch import Batch as BatchSchema

get_session = sessionmaker(bind=create_engine(Settings().database_url))
router = APIRouter()


@router.post('/add_batch', status_code=status.HTTP_201_CREATED)
def add_batch_endpoint(batch: BatchSchema):
    session = get_session()
    repo = SqlAlchemyRepository(session)

    services.add_batch(**batch.model_dump(), repo=repo, session=session)
    session.commit()
