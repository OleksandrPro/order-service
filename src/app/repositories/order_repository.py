from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db.manager import DatabaseManager
from app.db.models import Order as OrderModel, OrderItem as OrderItemModel
from app.schemas.order import OrderSnapshot, Order as OrderSchema


class OrderRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create(self, data: OrderSnapshot) -> OrderSchema:

        new_order = OrderModel(
            customer_id=data.customer_id,
            total_amount=data.total_amount,
            items=[
                OrderItemModel(
                    product_id=i.product_id,
                    quantity=i.quantity,
                    price_at_purchase=i.price_at_purchase,
                )
                for i in data.items
            ],
        )

        saved = self.db_manager.add_record(new_order)

        return OrderSchema.model_validate(saved, from_attributes=True)

    def get_by_customer(self, customer_id: int):
        return self.db_manager.get_all(
            select(OrderModel).where(OrderModel.customer_id == customer_id)
        )