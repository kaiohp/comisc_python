from http import HTTPStatus

from src.domain.models import Batch, OrderLine, allocate


@fastapi.route.something
def allocate_endpoint():
    session = start_session()

    line = OrderLine(body.orderid, body.product, body.quantity)

    batches = session.query(Batch).all()

    allocate(line, batches)

    session.commit()

    return HTTPStatus.CREATED
