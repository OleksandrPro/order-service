from sqlalchemy.orm import Session
from app.db.manager import DatabaseManager
from app.repositories import CustomerRepository
from app.services.customer_service import CustomerService


def get_customer_service(session: Session) -> CustomerService:
    db_manager = DatabaseManager(session)
    repo = CustomerRepository(db_manager)

    return CustomerService(repo)