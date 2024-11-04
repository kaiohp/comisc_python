from fastapi import APIRouter, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.models import OrderLine, allocate
from src.infra.database.config import Settings
from src.infra.database.repositories.repository import SqlAlchemyRepository
from src.main.models.order_line import OrderLine as OrderLineSchema

get_session = sessionmaker(bind=create_engine(Settings().database_url))
router = APIRouter()


@router.post('/allocate', status_code=status.HTTP_201_CREATED)
def allocate_endpoint(order_line: OrderLineSchema):
    session = get_session()
    batches = SqlAlchemyRepository(session).list()
    lines = OrderLine(**order_line.model_dump())
    batch_reference = allocate(lines, batches)

    session.commit()

    return {'batch_ref': batch_reference}
