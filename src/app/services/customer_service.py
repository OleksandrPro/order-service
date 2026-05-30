from app.repositories import CustomerRepository
from app.schemas import CreateCustomer, Customer
from app.exceptions.domain import CustomerCreationError


class CustomerService:
    def __init__(self, customer_repo: CustomerRepository):
        self.repo = customer_repo

    def create(self, data: CreateCustomer) -> Customer:
        customer = self.repo.create(data)
        if not customer:
            raise CustomerCreationError("Failed to create new customer")
        return customer