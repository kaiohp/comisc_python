from fastapi import APIRouter, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data import services
from src.domain.errors import OrderLineNotFound
from src.infra.database.config import Settings
from src.infra.database.repositories.repository import SqlAlchemyRepository
from src.main.models.order_line import OrderLine as OrderLineSchema

get_session = sessionmaker(bind=create_engine(Settings().database_url))
router = APIRouter()


@router.post('/deallocate', status_code=status.HTTP_202_ACCEPTED)
def deallocate_endpoint(order_line: OrderLineSchema):
    session = get_session()
    repo = SqlAlchemyRepository(session)

    try:
        batch_reference = services.deallocate(
            **order_line.model_dump(), repo=repo, session=session
        )
    except OrderLineNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err

    session.commit()
    return {'batch_ref': batch_reference}
