import pytest
from unittest.mock import MagicMock
from decimal import Decimal
from pydantic import ValidationError

from app.schemas.order import CreateOrder, CreateOrderItem
from app.exceptions.domain import (
    CustomerNotFoundError,
    ProductNotFoundError,
    InsufficientStockError,
)


class TestOrderService:

    def test_create_order_success(self, order_service, mock_uow, customer, product):
        mock_uow.customer_repo.get.return_value = customer
        mock_uow.product_repo.get_many.return_value = {1: product}
        mock_uow.order_repo.create.side_effect = lambda x: x

        data = CreateOrder(
            customer_id=1,
            items=[CreateOrderItem(product_id=1, quantity=1)],
        )

        result = order_service.create(data)

        assert mock_uow.customer_repo.get.called
        assert mock_uow.product_repo.get_many.called
        assert mock_uow.order_repo.create.called
        assert mock_uow.product_repo.update_stock.called

        snapshot = mock_uow.order_repo.create.call_args.args[0]

        assert snapshot.customer_id == 1
        assert snapshot.total_amount == Decimal("500.00")

        items = {i.product_id: i for i in snapshot.items}
        assert items[1].quantity == 1
        assert items[1].price_at_purchase == Decimal("500.00")

        assert result.customer_id == 1
        assert result.total_amount == Decimal("500.00")


    def test_create_order_customer_not_found(self, order_service, mock_uow):
        mock_uow.customer_repo.get.return_value = None

        data = CreateOrder(
            customer_id=99,
            items=[CreateOrderItem(product_id=1, quantity=1)],
        )

        with pytest.raises(CustomerNotFoundError) as exc:
            order_service.create(data)

        assert exc.value.customer_id == 99

        mock_uow.order_repo.create.assert_not_called()
        mock_uow.product_repo.update_stock.assert_not_called()


    def test_create_order_product_not_found(self, order_service, mock_uow, customer):
        mock_uow.customer_repo.get.return_value = customer
        mock_uow.product_repo.get_many.return_value = {}

        data = CreateOrder(
            customer_id=1,
            items=[CreateOrderItem(product_id=99, quantity=1)],
        )

        with pytest.raises(ProductNotFoundError) as exc:
            order_service.create(data)

        assert exc.value.product_id == 99

        mock_uow.order_repo.create.assert_not_called()


    def test_create_order_calculates_total_amount(
        self, order_service, mock_uow, customer, product_factory
    ):
        mock_uow.customer_repo.get.return_value = customer
        mock_uow.order_repo.create.side_effect = lambda x: x

        mock_uow.product_repo.get_many.return_value = {
            1: product_factory(id=1, price="100.00"),
            2: product_factory(id=2, price="50.00"),
        }

        data = CreateOrder(
            customer_id=1,
            items=[
                CreateOrderItem(product_id=1, quantity=2),
                CreateOrderItem(product_id=2, quantity=3),
            ],
        )

        result = order_service.create(data)

        assert result.total_amount == Decimal("350.00")


    def test_create_order_multiple_products_snapshot(
        self, order_service, mock_uow, customer, product_factory
    ):
        mock_uow.customer_repo.get.return_value = customer
        mock_uow.order_repo.create.side_effect = lambda x: x

        mock_uow.product_repo.get_many.return_value = {
            1: product_factory(id=1, price="100.00"),
            2: product_factory(id=2, price="50.00"),
        }

        data = CreateOrder(
            customer_id=1,
            items=[
                CreateOrderItem(product_id=1, quantity=2),
                CreateOrderItem(product_id=2, quantity=3),
            ],
        )

        result = order_service.create(data)

        snapshot = mock_uow.order_repo.create.call_args.args[0]

        items = {i.product_id: i for i in snapshot.items}

        assert items[1].quantity == 2
        assert items[2].quantity == 3
        assert items[1].price_at_purchase == Decimal("100.00")
        assert items[2].price_at_purchase == Decimal("50.00")


    def test_create_order_price_snapshot_is_taken(self, order_service, mock_uow, customer, product_factory):
        mock_uow.customer_repo.get.return_value = customer
        mock_uow.order_repo.create.side_effect = lambda x: x

        mock_uow.product_repo.get_many.return_value = {
            1: product_factory(id=1, price="123.45")
        }

        data = CreateOrder(
            customer_id=1,
            items=[CreateOrderItem(product_id=1, quantity=5)],
        )

        result = order_service.create(data)

        assert result.items[0].price_at_purchase == Decimal("123.45")


    def test_create_order_merges_duplicates_contract(self, order_service, mock_uow, customer, product_factory):
        mock_uow.customer_repo.get.return_value = customer
        mock_uow.order_repo.create.side_effect = lambda x: x

        mock_uow.product_repo.get_many.return_value = {
            1: product_factory(id=1, price="100.00")
        }

        data = CreateOrder(
            customer_id=1,
            items=[
                CreateOrderItem(product_id=1, quantity=2),
                CreateOrderItem(product_id=1, quantity=3),
            ],
        )

        result = order_service.create(data)

        snapshot = mock_uow.order_repo.create.call_args.args[0]

        assert len(snapshot.items) == 1
        assert snapshot.total_amount == Decimal("500.00")


    def test_create_order_mixed_products_not_found(self, order_service, mock_uow, customer, product_factory):
        mock_uow.customer_repo.get.return_value = customer
        mock_uow.product_repo.get_many.return_value = {
            1: product_factory(id=1, price="100.00")
        }

        data = CreateOrder(
            customer_id=1,
            items=[
                CreateOrderItem(product_id=1, quantity=1),
                CreateOrderItem(product_id=999, quantity=1),
            ],
        )

        with pytest.raises(ProductNotFoundError) as exc:
            order_service.create(data)

        assert exc.value.product_id == 999
        mock_uow.order_repo.create.assert_not_called()


    def test_create_order_validation_fails_when_items_empty(self):
        with pytest.raises(ValidationError):
            CreateOrder(customer_id=1, items=[])


    def test_create_order_insufficient_stock(self, order_service, mock_uow, customer, product_factory):
        mock_uow.customer_repo.get.return_value = customer
        mock_uow.product_repo.get_many.return_value = {
            1: product_factory(id=1, price="100.00", stock=2)
        }

        data = CreateOrder(
            customer_id=1,
            items=[CreateOrderItem(product_id=1, quantity=5)],
        )

        with pytest.raises(InsufficientStockError) as exc:
            order_service.create(data)

        assert exc.value.product_id == 1
        assert exc.value.requested == 5
        assert exc.value.in_stock == 2

        mock_uow.order_repo.create.assert_not_called()
        mock_uow.product_repo.update_stock.assert_not_called()

    def test_list_by_customer_returns_orders(self, order_service, mock_uow):
        # Arrange
        orders = [MagicMock(), MagicMock()]

        mock_uow.order_repo.get_by_customer.return_value = orders

        # Act
        result = order_service.list_by_customer(10)

        # Assert
        mock_uow.order_repo.get_by_customer.assert_called_once_with(10)
        assert result == orders

    def test_list_by_customer_returns_empty_list_when_no_orders(self, order_service, mock_uow):
        # Arrange
        mock_uow.order_repo.get_by_customer.return_value = []

        # Act
        result = order_service.list_by_customer(999)

        # Assert
        mock_uow.order_repo.get_by_customer.assert_called_once_with(999)
        assert result == []