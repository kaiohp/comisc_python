from fastapi import APIRouter, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.errors import OutOfStock
from src.domain.models import OrderLine, allocate
from src.domain.models.batch import Batch
from src.infra.database.config import Settings
from src.infra.database.repositories.repository import SqlAlchemyRepository
from src.main.models.order_line import OrderLine as OrderLineSchema

get_session = sessionmaker(bind=create_engine(Settings().database_url))
router = APIRouter()


def is_valid_sku(sku, batches: list[Batch]):
    return sku in {batch.sku for batch in batches}


@router.post('/allocate', status_code=status.HTTP_201_CREATED)
def allocate_endpoint(order_line: OrderLineSchema):
    session = get_session()
    batches = SqlAlchemyRepository(session).list()
    line = OrderLine(**order_line.model_dump())

    if not is_valid_sku(line.sku, batches):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Invalid sku {line.sku}',
        )

    try:
        batch_reference = allocate(line, batches)
    except OutOfStock as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    session.commit()
    return {'batch_ref': batch_reference}
