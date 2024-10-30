from http import HTTPStatus

from src.domain.models import OrderLine, allocate
from src.infra.database.repositories.repository import SqlAlchemyRepository


@fastapi.route.something
def allocate_endpoint():
    session = start_session()
    batches = SqlAlchemyRepository(session).list()
    lines = [
        OrderLine(record.orderid, record.product, record.quantity)
        for record in request.body
    ]

    allocate(lines, batches)

    session.commit()

    return HTTPStatus.CREATED
