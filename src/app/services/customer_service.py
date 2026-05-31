from app.db.unit_of_work import UnitOfWork
from app.repositories import CustomerRepository
from app.schemas import CreateCustomer, Customer
from app.exceptions.domain import CustomerCreationError


class CustomerService:
    def __init__(
        self,
        customer_repo: CustomerRepository,
        uow: UnitOfWork,
    ):
        self.customer_repo = customer_repo
        self.uow = uow

    def create(self, data: CreateCustomer) -> Customer:
        with self.uow:
            customer = self.customer_repo.create(data)

        return customer