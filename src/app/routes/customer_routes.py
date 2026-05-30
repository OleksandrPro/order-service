from flask import Blueprint, request
from app.db.session import SessionFactory
from app.dependencies import get_customer_service
from app.schemas import CreateCustomer, Customer


customer_bp = Blueprint('customers', __name__, url_prefix='/customers')


@customer_bp.get('/<int:customer_id>')
def get_users(customer_id: int):
    return {"customer_id": customer_id, "name": "Alex"}, 200

@customer_bp.post('/')
def create_user():
    data = CreateCustomer.model_validate(request.get_json())
    with SessionFactory() as session:
        service = get_customer_service(session)

        customer = service.create(data)

        return customer.model_dump(), 201
    
@customer_bp.get("/<int:customer_id>/orders")
def get_customer_orders(customer_id):
    orders = order_service.get_by_customer(customer_id)
    return [Order.model_validate(o).model_dump() for o in orders]
