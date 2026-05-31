from decimal import Decimal
from app.db.unit_of_work import UnitOfWork
from app.schemas.order import (
    CreateOrder,
    Order as OrderSchema,
    OrderItemSnapshot,
    OrderSnapshot,
)
from app.schemas import ProductStockUpdate
from app.exceptions.domain import (
    CustomerNotFoundError,
    ProductNotFoundError,
    InsufficientStockError
)
from app.services.helpers.order_items_normalizer import (
    OrderItemsNormalizer,
)


class OrderService:
    def __init__(
        self, 
        uow: UnitOfWork
    ):
        self.uow = uow

    def create(self, data: CreateOrder) -> OrderSchema:

        with self.uow:
            customer = self.uow.customer_repo.get(data.customer_id)
            if not customer:
                raise CustomerNotFoundError(data.customer_id)
            
            normalized_items = OrderItemsNormalizer.merge_duplicates(data.items)    

            product_ids = [
                item.product_id
                for item in normalized_items
            ]

            products = self.uow.product_repo.get_many(product_ids)

            items_snapshot: list[OrderItemSnapshot] = []
            stock_updates: list[ProductStockUpdate] = []
            total = Decimal("0")

            for item in normalized_items:
                product = products.get(item.product_id)

                if not product:
                    raise ProductNotFoundError(item.product_id)
                
                if item.quantity > product.stock:
                    raise InsufficientStockError(
                        item.product_id, 
                        requested=item.quantity,
                        in_stock=product.stock
                    )

                snapshot_item = OrderItemSnapshot(
                    product_id=product.id,
                    quantity=item.quantity,
                    price_at_purchase=product.price,
                )

                stock_update = ProductStockUpdate(
                    product_id=product.id,
                    stock=product.stock - item.quantity,
                )

                items_snapshot.append(snapshot_item)
                stock_updates.append(stock_update)
                total += product.price * item.quantity

            order_snapshot = OrderSnapshot(
                customer_id=data.customer_id,
                items=items_snapshot,
                total_amount=total,
            )
        
            order = self.uow.order_repo.create(order_snapshot)
            self.uow.product_repo.update_stock(stock_updates)

        return order