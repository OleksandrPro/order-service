from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db.manager import DatabaseManager
from app.db.models import Customer as CustomerModel 
from app.schemas import CreateCustomer, Customer
from app.exceptions.domain import EmailAlreadyTakenError

class CustomerRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create(self, data: CreateCustomer) -> Customer:
        try:
            new_customer = CustomerModel(**data.model_dump())

            saved_customer = self.db_manager.add_record(new_customer)

            return Customer.model_validate(saved_customer)

        except IntegrityError:
            raise EmailAlreadyTakenError(data.email)
    
    def get(self, customer_id: int) -> Customer | None:
        query = select(CustomerModel).where(CustomerModel.id == customer_id)
        retrieved_customer = self.db_manager.get_first(query)

        if retrieved_customer is None:
            return None

        return Customer.model_validate(retrieved_customer)
    
    def get_all(self) -> list[Customer]:
        query = select(CustomerModel)
        all_customers = self.db_manager.get_all(query)

        return [Customer.model_validate(customer) for customer in all_customers]