from sqlalchemy.orm import Session
from app.db.manager import DatabaseManager
from app.db.unit_of_work import UnitOfWork
from app.repositories import CustomerRepository
from app.services.customer_service import CustomerService

from app.repositories import ProductRepository
from app.services.product_service import ProductService

from app.repositories import OrderRepository
from app.services.order_service import OrderService


def get_customer_repository(session: Session) -> CustomerRepository:
    return CustomerRepository(DatabaseManager(session))

def get_product_repository(session: Session) -> ProductRepository:
    return ProductRepository(DatabaseManager(session))

def get_order_repository(session: Session) -> OrderRepository:
    return OrderRepository(DatabaseManager(session))

def get_uow(session: Session) -> UnitOfWork:
    return UnitOfWork(DatabaseManager(session))

def get_customer_service(session: Session) -> CustomerService:
    repo = get_customer_repository(session)
    uow = get_uow(session)
    return CustomerService(repo, uow=uow)


def get_product_service(session: Session) -> ProductService:
    repo = get_product_repository(session)
    uow = get_uow(session)
    return ProductService(repo, uow=uow)


def get_order_service(session: Session) -> OrderService:
    order_repo = get_order_repository(session)
    customer_repo = get_customer_repository(session)
    product_repo = get_product_repository(session)
    uow = get_uow(session)
    
    return OrderService(
        order_repo=order_repo,
        customer_repo=customer_repo,
        product_repo=product_repo,
        uow=uow
    )