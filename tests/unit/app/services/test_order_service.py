import pytest
from decimal import Decimal
from pydantic import ValidationError

from app.schemas.order import CreateOrder, CreateOrderItem
from app.exceptions.domain import CustomerNotFoundError, ProductNotFoundError

class TestOrderService:

    def test_create_order_success(
        self, order_service, mock_order_repo, mock_customer_repo, mock_product_repo, customer, product
    ):
        # Arrange
        mock_customer_repo.get.return_value = customer
        
        mock_product_repo.get_many.return_value = {1: product}
        
        mock_order_repo.create.side_effect = lambda snapshot: snapshot 
        
        data = CreateOrder(customer_id=1, items=[CreateOrderItem(product_id=1, quantity=1)])

        # Act
        result = order_service.create(data)

        # Assert
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get_many.assert_called_once_with([1])
        mock_order_repo.create.assert_called_once()

        snapshot = mock_order_repo.create.call_args.args[0]
        assert snapshot.customer_id == 1
        assert snapshot.total_amount == Decimal("500.00")
        assert len(snapshot.items) == 1
        assert snapshot.items[0].product_id == 1
        assert snapshot.items[0].quantity == 1
        assert snapshot.items[0].price_at_purchase == Decimal("500.00")

        assert result.customer_id == 1
        assert result.total_amount == Decimal("500.00")
        assert len(result.items) == 1
        assert result.items[0].product_id == 1
        assert result.items[0].quantity == 1
        assert result.items[0].price_at_purchase == Decimal("500.00")

    def test_create_order_customer_not_found(
        self, order_service, mock_order_repo, mock_customer_repo, mock_product_repo
    ):
        # Arrange
        mock_customer_repo.get.return_value = None
        
        data = CreateOrder(customer_id=99, items=[CreateOrderItem(product_id=1, quantity=1)])

        # Act and Assert
        with pytest.raises(CustomerNotFoundError) as exc_info:
            order_service.create(data)
        
        assert exc_info.value.customer_id == 99
        mock_customer_repo.get.assert_called_once_with(99)
        mock_order_repo.create.assert_not_called()

    def test_create_order_product_not_found(
        self, order_service, mock_order_repo, mock_customer_repo, mock_product_repo, customer
    ):
        # Arrange
        mock_customer_repo.get.return_value = customer
        
        mock_product_repo.get_many.return_value = {}
        
        data = CreateOrder(customer_id=1, items=[CreateOrderItem(product_id=99, quantity=1)])

        # Act and Assert
        with pytest.raises(ProductNotFoundError) as exc_info:
            order_service.create(data)
        
        assert exc_info.value.product_id == 99
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get_many.assert_called_once_with([99])
        mock_order_repo.create.assert_not_called()

    def test_create_order_calculates_total_amount(
        self, order_service, mock_order_repo, mock_customer_repo, mock_product_repo, customer, product_factory
    ):
        # Arrange
        mock_customer_repo.get.return_value = customer
        mock_order_repo.create.side_effect = lambda snapshot: snapshot
        
        mock_product_repo.get_many.return_value = {
            1: product_factory(id=1, price="100.00"),
            2: product_factory(id=2, price="50.00"),
        }
        
        data = CreateOrder(
            customer_id=1, 
            items=[
                CreateOrderItem(product_id=1, quantity=2),
                CreateOrderItem(product_id=2, quantity=3)
            ]
        )

        # Act
        result = order_service.create(data)

        # Assert
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get_many.assert_called_once_with([1, 2])
        assert result.total_amount == Decimal("350.00")

    def test_create_order_with_multiple_products(
        self, order_service, mock_order_repo, mock_customer_repo, mock_product_repo, customer, product_factory
    ):
        # Arrange
        mock_customer_repo.get.return_value = customer
        mock_order_repo.create.side_effect = lambda snapshot: snapshot
        
        mock_product_repo.get_many.return_value = {
            1: product_factory(id=1, price="100.00"),
            2: product_factory(id=2, price="50.00"),
        }
        
        data = CreateOrder(
            customer_id=1, 
            items=[
                CreateOrderItem(product_id=1, quantity=2),
                CreateOrderItem(product_id=2, quantity=3)
            ]
        )

        # Act
        result = order_service.create(data)

        # Assert
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get_many.assert_called_once_with([1, 2])
        mock_order_repo.create.assert_called_once()

        snapshot = mock_order_repo.create.call_args.args[0]
        assert len(snapshot.items) == 2
        assert snapshot.items[0].product_id == 1
        assert snapshot.items[0].quantity == 2
        assert snapshot.items[0].price_at_purchase == Decimal("100.00")
        assert snapshot.items[1].product_id == 2
        assert snapshot.items[1].quantity == 3
        assert snapshot.items[1].price_at_purchase == Decimal("50.00")

        assert len(result.items) == 2
        assert result.items[0].product_id == 1
        assert result.items[0].quantity == 2
        assert result.items[0].price_at_purchase == Decimal("100.00")
        assert result.items[1].product_id == 2
        assert result.items[1].quantity == 3
        assert result.items[1].price_at_purchase == Decimal("50.00")

    def test_create_order_stores_price_snapshot(
        self, order_service, mock_order_repo, mock_customer_repo, mock_product_repo, customer, product_factory
    ):
        # Arrange
        mock_customer_repo.get.return_value = customer
        mock_order_repo.create.side_effect = lambda snapshot: snapshot
        
        mock_product_repo.get_many.return_value = {
            1: product_factory(id=1, price="123.45")
        }
        
        data = CreateOrder(customer_id=1, items=[CreateOrderItem(product_id=1, quantity=5)])

        # Act
        result = order_service.create(data)

        # Assert
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get_many.assert_called_once_with([1])
        assert result.items[0].price_at_purchase == Decimal("123.45")
        assert result.items[0].quantity == 5

    def test_create_order_validation_fails_when_items_empty(self):
        # Act and Assert
        with pytest.raises(ValidationError):
            CreateOrder(
                customer_id=1,
                items=[]
            )
    
    def test_create_order_merges_duplicate_products(
        self, order_service, mock_order_repo, mock_customer_repo, mock_product_repo, customer, product_factory
    ):
        # Arrange
        mock_customer_repo.get.return_value = customer
        mock_order_repo.create.side_effect = lambda snapshot: snapshot
        
        mock_product_repo.get_many.return_value = {
            1: product_factory(id=1, price="100.00")
        }
        
        data = CreateOrder(
            customer_id=1, 
            items=[
                CreateOrderItem(product_id=1, quantity=2),
                CreateOrderItem(product_id=1, quantity=3)
            ]
        )

        # Act
        result = order_service.create(data)

        # Assert
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get_many.assert_called_once_with([1])
        mock_order_repo.create.assert_called_once()

        snapshot = mock_order_repo.create.call_args.args[0]
        assert len(snapshot.items) == 1
        assert snapshot.items[0].product_id == 1
        assert snapshot.items[0].quantity == 5
        assert snapshot.items[0].price_at_purchase == Decimal("100.00")
        assert snapshot.total_amount == Decimal("500.00")

        assert len(result.items) == 1
        assert result.items[0].product_id == 1
        assert result.items[0].quantity == 5
        assert result.items[0].price_at_purchase == Decimal("100.00")
        assert result.total_amount == Decimal("500.00")

    def test_create_order_mixed_products_not_found(
        self, order_service, mock_order_repo, mock_customer_repo, mock_product_repo, customer, product_factory
    ):
        # Arrange
        mock_customer_repo.get.return_value = customer
        
        mock_product_repo.get_many.return_value = {
            1: product_factory(id=1, price="100.00")
        }
        
        data = CreateOrder(
            customer_id=1, 
            items=[
                CreateOrderItem(product_id=1, quantity=1),
                CreateOrderItem(product_id=999, quantity=1)
            ]
        )

        # Act and Assert
        with pytest.raises(ProductNotFoundError) as exc_info:
            order_service.create(data)
            
        # Assert
        assert exc_info.value.product_id == 999
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get_many.assert_called_once_with([1, 999])
        mock_order_repo.create.assert_not_called()