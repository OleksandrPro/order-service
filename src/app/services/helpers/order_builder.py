from decimal import Decimal
from app.schemas import (
    CreateOrderItem,
    OrderItemSnapshot, 
    OrderSnapshot,
    ProductStockUpdate, 
    Product    
) 
from app.exceptions.domain import ProductNotFoundError, InsufficientStockError
from app.services.helpers.order_items_normalizer import OrderItemsNormalizer


class OrderBuilder:
    @staticmethod
    def build(customer_id, items: list[CreateOrderItem], products: dict[int, Product]):
        normalized_items = OrderItemsNormalizer.merge_duplicates(items)

        items_snapshot = []
        stock_updates = []
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

            items_snapshot.append(
                OrderItemSnapshot(
                    product_id=product.id,
                    quantity=item.quantity,
                    price_at_purchase=product.price,
                )
            )

            stock_updates.append(
                ProductStockUpdate(
                    product_id=product.id,
                    stock=product.stock - item.quantity,
                )
            )

            total += product.price * item.quantity

        order_snapshot = OrderSnapshot(
            customer_id=customer_id,
            items=items_snapshot,
            total_amount=total,
        )

        return order_snapshot, stock_updates