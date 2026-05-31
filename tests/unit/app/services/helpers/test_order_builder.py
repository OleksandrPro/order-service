import pytest
from decimal import Decimal

from app.services.helpers import OrderBuilder
from app.exceptions.domain import ProductNotFoundError, InsufficientStockError
from app.schemas.order import CreateOrderItem


class TestOrderBuilder:

    def test_build_snapshot_correctness(self, product_factory):
        # Arrange
        items = [
            CreateOrderItem(product_id=1, quantity=2),
            CreateOrderItem(product_id=2, quantity=1)
        ]

        products = {
            1: product_factory(id=1, price="100.00", stock=5),
            2: product_factory(id=2, price="50.00", stock=2)
        }

        # Act
        order_snapshot, stock_updates = OrderBuilder.build(
            customer_id=1,
            items=items,
            products=products
        )

        # Assert
        assert order_snapshot.customer_id == 1
        assert order_snapshot.total_amount == Decimal("250.00")
        assert len(order_snapshot.items) == 2

        assert {i.product_id for i in order_snapshot.items} == {1, 2}

        assert len(stock_updates) == 2

        stock_map = {u.product_id: u.stock for u in stock_updates}
        assert stock_map[1] == 3
        assert stock_map[2] == 1

    def test_builder_raises_insufficient_stock(self, product_factory):
        items = [CreateOrderItem(product_id=1, quantity=10)]

        products = {
            1: product_factory(id=1, price="100.00", stock=5)
        }

        with pytest.raises(InsufficientStockError) as exc:
            OrderBuilder.build(customer_id=1, items=items, products=products)

        assert exc.value.product_id == 1
        assert exc.value.requested == 10
        assert exc.value.in_stock == 5

    def test_builder_raises_product_not_found(self, product_factory):
        items = [CreateOrderItem(product_id=99, quantity=1)]

        products = {
            1: product_factory(id=1, price="100.00", stock=5)
        }

        with pytest.raises(ProductNotFoundError) as exc:
            OrderBuilder.build(customer_id=1, items=items, products=products)

        assert exc.value.product_id == 99

    def test_builder_is_deterministic(self, product_factory):
        items = [CreateOrderItem(product_id=1, quantity=2)]

        products = {
            1: product_factory(id=1, price="100.00", stock=5)
        }

        result1 = OrderBuilder.build(customer_id=1, items=items, products=products)
        result2 = OrderBuilder.build(customer_id=1, items=items, products=products)

        assert result1 == result2

    def test_builder_does_not_mutate_inputs(self, product_factory):
        # Arrange
        items = [CreateOrderItem(product_id=1, quantity=2)]
        products = {
            1: product_factory(id=1, price="100.00", stock=5)
        }

        items_before = items.copy()
        products_before = products.copy()

        # Act
        OrderBuilder.build(customer_id=1, items=items, products=products)

        # Assert
        assert items == items_before
        assert products == products_before