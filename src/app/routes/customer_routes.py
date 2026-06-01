from flask import Blueprint, request
from app.db.session import SessionFactory
from app.dependencies import get_customer_service, get_order_service
from app.schemas import CreateCustomer, Order


customer_bp = Blueprint('customers', __name__, url_prefix='/customers')


@customer_bp.post('/')
def create_user():
    data = CreateCustomer.model_validate(request.get_json())
    with SessionFactory() as session:
        service = get_customer_service(session)

        customer = service.create(data)

        return customer.model_dump(), 201

@customer_bp.get("/")
def get_all_customers():
    with SessionFactory() as session:
        service = get_customer_service(session)

        customers = service.get_all()

        return [customer.model_dump() for customer in customers], 200

@customer_bp.get("/<int:customer_id>/orders")
def get_customer_orders(customer_id):
    with SessionFactory() as session:
        service = get_order_service(session)

        orders = service.list_by_customer(customer_id)

        return [order.model_dump() for order in orders], 200
