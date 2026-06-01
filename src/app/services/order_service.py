from app.db.unit_of_work import UnitOfWork
from app.schemas import (
    CreateOrder,
    Order
)
from app.exceptions.domain import (
    CustomerNotFoundError,
)
from app.services.helpers import (
    OrderBuilder
)


class OrderService:
    def __init__(
        self, 
        uow: UnitOfWork
    ):
        self.uow = uow

    def create(self, data: CreateOrder):

        with self.uow:
            customer = self.uow.customer_repo.get(data.customer_id)
            if not customer:
                raise CustomerNotFoundError(data.customer_id)

            product_ids = [i.product_id for i in data.items]
            products = self.uow.product_repo.get_many(product_ids)

            order_snapshot, stock_updates = OrderBuilder.build(
                customer_id=data.customer_id,
                items=data.items,
                products=products,
            )

            order = self.uow.order_repo.create(order_snapshot)
            self.uow.product_repo.update_stock(stock_updates)

        return order
    
    def list_by_customer(self, customer_id: int) -> list[Order]:
        with self.uow:
            customer = self.uow.customer_repo.get(customer_id)

            if not customer:
                raise CustomerNotFoundError(customer_id)

            orders = self.uow.order_repo.get_by_customer(customer_id)

        return orders