from app.db.unit_of_work import UnitOfWork
from app.schemas import CreateCustomer, Customer


class CustomerService:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

    def create(self, data: CreateCustomer) -> Customer:
        with self.uow:
            customer = self.uow.customer_repo.create(data)

        return customer
    
    def get_all(self) -> list[Customer]:
        with self.uow:
            customers = self.uow.customer_repo.get_all()

        return customers