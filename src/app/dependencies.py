from sqlalchemy.orm import Session
from app.db.manager import DatabaseManager
from app.repositories import CustomerRepository
from app.services.customer_service import CustomerService

from app.db.manager import DatabaseManager
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


def get_customer_service(session: Session) -> CustomerService:
    db_manager = DatabaseManager(session)
    repo = CustomerRepository(db_manager)

    return CustomerService(repo)

def get_product_service(session: Session) -> ProductService:
    db_manager = DatabaseManager(session)
    repo = ProductRepository(db_manager)

    return ProductService(repo)