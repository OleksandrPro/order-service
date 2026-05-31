import pytest
from datetime import datetime
from decimal import Decimal
from pydantic import ValidationError

from app.schemas.customer import Customer
from app.schemas.product import Product
from app.schemas.order import CreateOrder, CreateOrderItem
from app.exceptions.domain import CustomerNotFoundError, ProductNotFoundError
from app.services.order_service import OrderService

class TestOrderService:

    def test_create_order_success(self, mock_order_repo, mock_customer_repo, mock_product_repo):
        # Arrange
        mock_customer_repo.get.return_value = Customer(
            id=1, name="John Doe", email="john@example.com", created_at=datetime.now()
        )
        
        mock_product_repo.get.return_value = Product(
            id=1, name="Laptop", sku="LAP-123", price=Decimal("500.00"), stock=10
        )
        
        mock_order_repo.create.side_effect = lambda snapshot: snapshot 
        
        service = OrderService(mock_order_repo, mock_customer_repo, mock_product_repo)
        data = CreateOrder(customer_id=1, items=[CreateOrderItem(product_id=1, quantity=1)])

        # Act
        result = service.create(data)

        # Assert
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get.assert_called_once_with(1)
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

    def test_create_order_customer_not_found(self, mock_order_repo, mock_customer_repo, mock_product_repo):
        # Arrange
        mock_customer_repo.get.return_value = None
        
        service = OrderService(mock_order_repo, mock_customer_repo, mock_product_repo)
        data = CreateOrder(customer_id=99, items=[CreateOrderItem(product_id=1, quantity=1)])

        # Act and Assert
        with pytest.raises(CustomerNotFoundError):
            service.create(data)
        
        mock_customer_repo.get.assert_called_once_with(99)
        mock_order_repo.create.assert_not_called()

    def test_create_order_product_not_found(self, mock_order_repo, mock_customer_repo, mock_product_repo):
        # Arrange
        mock_customer_repo.get.return_value = Customer(
            id=1, name="John Doe", email="john@example.com", created_at=datetime.now()
        )
        mock_product_repo.get.return_value = None
        
        service = OrderService(mock_order_repo, mock_customer_repo, mock_product_repo)
        data = CreateOrder(customer_id=1, items=[CreateOrderItem(product_id=99, quantity=1)])

        # Act and Assert
        with pytest.raises(ProductNotFoundError):
            service.create(data)
            
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get.assert_called_once_with(99)
        mock_order_repo.create.assert_not_called()

    def test_create_order_calculates_total_amount(self, mock_order_repo, mock_customer_repo, mock_product_repo):
        # Arrange
        mock_customer_repo.get.return_value = Customer(
            id=1, name="John Doe", email="john@example.com", created_at=datetime.now()
        )
        mock_order_repo.create.side_effect = lambda snapshot: snapshot
        
        def get_product_mock(product_id):
            if product_id == 1:
                return Product(id=1, name="Keyboard", sku="KB-1", price=Decimal("100.00"), stock=10)
            if product_id == 2:
                return Product(id=2, name="Mouse", sku="M-1", price=Decimal("50.00"), stock=10)
            return None
            
        mock_product_repo.get.side_effect = get_product_mock
        
        service = OrderService(mock_order_repo, mock_customer_repo, mock_product_repo)
        
        data = CreateOrder(
            customer_id=1, 
            items=[
                CreateOrderItem(product_id=1, quantity=2),
                CreateOrderItem(product_id=2, quantity=3)
            ]
        )

        # Act
        result = service.create(data)

        # Assert
        mock_customer_repo.get.assert_called_once_with(1)
        assert mock_product_repo.get.call_count == 2
        assert result.total_amount == Decimal("350.00")

    def test_create_order_with_multiple_products(self, mock_order_repo, mock_customer_repo, mock_product_repo):
        # Arrange
        mock_customer_repo.get.return_value = Customer(
            id=1, name="John Doe", email="john@example.com", created_at=datetime.now()
        )
        mock_order_repo.create.side_effect = lambda snapshot: snapshot
        
        def get_product_mock(product_id):
            if product_id == 1:
                return Product(id=1, name="Keyboard", sku="KB-1", price=Decimal("100.00"), stock=10)
            if product_id == 2:
                return Product(id=2, name="Mouse", sku="M-1", price=Decimal("50.00"), stock=10)
            return None
            
        mock_product_repo.get.side_effect = get_product_mock
        
        service = OrderService(mock_order_repo, mock_customer_repo, mock_product_repo)
        
        data = CreateOrder(
            customer_id=1, 
            items=[
                CreateOrderItem(product_id=1, quantity=2),
                CreateOrderItem(product_id=2, quantity=3)
            ]
        )

        # Act
        result = service.create(data)

        # Assert
        mock_customer_repo.get.assert_called_once_with(1)
        assert mock_product_repo.get.call_count == 2
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

    def test_create_order_stores_price_snapshot(self, mock_order_repo, mock_customer_repo, mock_product_repo):
        # Arrange
        mock_customer_repo.get.return_value = Customer(
            id=1, name="John Doe", email="john@example.com", created_at=datetime.now()
        )
        mock_order_repo.create.side_effect = lambda snapshot: snapshot
        
        product_price = Decimal("123.45")
        mock_product_repo.get.return_value = Product(
            id=1, name="Monitor", sku="MN-1", price=product_price, stock=5
        )
        
        service = OrderService(mock_order_repo, mock_customer_repo, mock_product_repo)
        data = CreateOrder(customer_id=1, items=[CreateOrderItem(product_id=1, quantity=5)])

        # Act
        result = service.create(data)

        # Assert
        mock_customer_repo.get.assert_called_once_with(1)
        mock_product_repo.get.assert_called_once_with(1)
        assert result.items[0].price_at_purchase == product_price
        assert result.items[0].quantity == 5

    def test_create_order_validation_fails_when_items_empty(self):
        # Act and Assert
        with pytest.raises(ValidationError):
            CreateOrder(
                customer_id=1,
                items=[]
            )