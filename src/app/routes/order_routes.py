from flask import Blueprint, request
from app.db.session import SessionFactory
from app.dependencies import get_order_service
from app.schemas import CreateOrder, Order


order_bp = Blueprint('orders', __name__, url_prefix='/orders')


@order_bp.post("/")
def create_order():
    data = CreateOrder.model_validate(request.get_json())

    with SessionFactory() as session:
        service = get_order_service(session)
        order = service.create(data)

        return order.model_dump(), 201
