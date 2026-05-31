import pytest
from datetime import datetime
from decimal import Decimal

from app.schemas.customer import Customer
from app.schemas.product import Product
from app.services.order_service import OrderService
from app.services.customer_service import CustomerService
from app.services.product_service import ProductService

@pytest.fixture
def customer():
    return Customer(
        id=1,
        name="John Doe",
        email="john@example.com",
        created_at=datetime.now(),
    )

@pytest.fixture
def product():
    return Product(
        id=1,
        name="Laptop",
        sku="LAP-123",
        price=Decimal("500.00"),
        stock=10,
    )

@pytest.fixture
def product_factory():
    def factory(id: int, price: str = "100.00", stock: int = 10):
        return Product(
            id=id,
            name=f"Product {id}",
            sku=f"SKU-{id}",
            price=Decimal(price),
            stock=stock,
        )
    return factory

@pytest.fixture
def customer_service(mock_customer_repo):
    return CustomerService(mock_customer_repo)

@pytest.fixture
def product_service(mock_product_repo):
    return ProductService(mock_product_repo)

@pytest.fixture
def order_service(mock_order_repo, mock_customer_repo, mock_product_repo):
    return OrderService(
        order_repo=mock_order_repo,
        customer_repo=mock_customer_repo,
        product_repo=mock_product_repo,
    )