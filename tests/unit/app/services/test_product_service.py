import pytest
from decimal import Decimal
from app.schemas.product import CreateProduct, Product
from app.exceptions.domain import SKUAlreadyExistsError 
from app.services.product_service import ProductService

class TestProductService:

    def test_create_product_success(self, mock_product_repo):
        # Arrange
        data = CreateProduct(name="Laptop", sku="LAP-123", price=Decimal("1500.00"))
        
        expected_product = Product(
            id=1,
            name="Laptop",
            sku="LAP-123",
            price=Decimal("1500.00"),
            stock=10
        )
        mock_product_repo.create.return_value = expected_product
        
        service = ProductService(mock_product_repo)

        # Act
        result = service.create(data)

        # Assert
        mock_product_repo.create.assert_called_once_with(data)
        assert result.id == 1
        assert result.name == "Laptop"
        assert result.sku == "LAP-123"
        assert result.price == Decimal("1500.00")

    def test_create_product_raises_when_sku_exists(self, mock_product_repo):
        # Arrange
        data = CreateProduct(name="Laptop", sku="DUPLICATE-SKU", price=Decimal("1500.00"))
        
        mock_product_repo.create.side_effect = SKUAlreadyExistsError("DUPLICATE-SKU")
        
        service = ProductService(mock_product_repo)

        # Act and Assert
        with pytest.raises(SKUAlreadyExistsError):
            service.create(data)