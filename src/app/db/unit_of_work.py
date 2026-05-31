from .manager import DatabaseManager
from app.repositories import (
    CustomerRepository,
    ProductRepository,
    OrderRepository
)

class UnitOfWork:
    def __init__(
            self, 
            db_manager: DatabaseManager,
            customer_repo: CustomerRepository,
            product_repo: ProductRepository,
            order_repo: OrderRepository
    ):
        self.db_manager = db_manager
        self.customer_repo = customer_repo
        self.product_repo = product_repo
        self.order_repo = order_repo

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc:
            self.db_manager.session.rollback()
        else:
            self.db_manager.commit()