from fastapi import APIRouter, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data import services
from src.domain.errors import OutOfStock
from src.domain.models import OrderLine
from src.infra.database.config import Settings
from src.infra.database.repositories.repository import SqlAlchemyRepository
from src.main.models.order_line import OrderLine as OrderLineSchema

get_session = sessionmaker(bind=create_engine(Settings().database_url))
router = APIRouter()


@router.post('/allocate', status_code=status.HTTP_201_CREATED)
def allocate_endpoint(order_line: OrderLineSchema):
    session = get_session()
    repo = SqlAlchemyRepository(session)
    line = OrderLine(**order_line.model_dump())

    try:
        batch_reference = services.allocate(line, repo, session)
    except (OutOfStock, services.InvalidSku) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e

    session.commit()
    return {'batch_ref': batch_reference}
