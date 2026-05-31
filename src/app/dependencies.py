from sqlalchemy.orm import Session
from app.db.manager import DatabaseManager
from app.db.unit_of_work import UnitOfWork
from app.repositories import CustomerRepository
from app.services.customer_service import CustomerService

from app.repositories import ProductRepository
from app.services.product_service import ProductService

from app.repositories import OrderRepository
from app.services.order_service import OrderService


def get_db_manager(session: Session) -> DatabaseManager:
    return DatabaseManager(session)

def get_customer_repository(db_manager: DatabaseManager) -> CustomerRepository:
    return CustomerRepository(db_manager)

def get_product_repository(db_manager: DatabaseManager) -> ProductRepository:
    return ProductRepository(db_manager)

def get_order_repository(db_manager: DatabaseManager) -> OrderRepository:
    return OrderRepository(db_manager)

def get_uow(session: Session) -> UnitOfWork:
    db_manager = get_db_manager(session)
    customer_repo = get_customer_repository(db_manager)
    product_repo = get_product_repository(db_manager)
    order_repo = get_order_repository(db_manager)
    return UnitOfWork(db_manager, customer_repo, product_repo, order_repo)

def get_customer_service(session: Session) -> CustomerService:
    uow = get_uow(session)
    return CustomerService(uow=uow)

def get_product_service(session: Session) -> ProductService:
    uow = get_uow(session)
    return ProductService(uow=uow)

def get_order_service(session: Session) -> OrderService:
    uow = get_uow(session)
    return OrderService(uow=uow)