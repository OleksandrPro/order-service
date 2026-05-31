from decimal import Decimal
from app.repositories import CustomerRepository, ProductRepository, OrderRepository
from app.schemas.order import (
    CreateOrder,
    Order as OrderSchema,
    OrderItemSnapshot,
    OrderSnapshot,
)
from app.exceptions.domain import (
    CustomerNotFoundError,
    ProductNotFoundError
)
from app.services.helpers.order_items_normalizer import (
    OrderItemsNormalizer,
)


class OrderService:
    def __init__(
            self, 
            order_repo: OrderRepository, 
            customer_repo: CustomerRepository, 
            product_repo: ProductRepository
    ):
        self.order_repo = order_repo
        self.customer_repo = customer_repo
        self.product_repo = product_repo

    def create(self, data: CreateOrder) -> OrderSchema:

        customer = self.customer_repo.get(data.customer_id)
        if not customer:
            raise CustomerNotFoundError(data.customer_id)
        
        normalized_items = OrderItemsNormalizer.merge_duplicates(data.items)    

        product_ids = [
            item.product_id
            for item in normalized_items
        ]

        products = self.product_repo.get_many(product_ids)

        items_snapshot: list[OrderItemSnapshot] = []
        total = Decimal("0")

        for item in normalized_items:
            product = products.get(item.product_id)

            if not product:
                raise ProductNotFoundError(item.product_id)

            snapshot_item = OrderItemSnapshot(
                product_id=product.id,
                quantity=item.quantity,
                price_at_purchase=product.price,
            )

            items_snapshot.append(snapshot_item)
            total += product.price * item.quantity

        order_snapshot = OrderSnapshot(
            customer_id=data.customer_id,
            items=items_snapshot,
            total_amount=total,
        )

        return self.order_repo.create(order_snapshot)