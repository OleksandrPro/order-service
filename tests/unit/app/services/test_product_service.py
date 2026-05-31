import pytest
from decimal import Decimal
from app.schemas.product import CreateProduct
from app.exceptions.domain import SKUAlreadyExistsError 

class TestProductService:

    def test_create_product_success(self, product_service, mock_product_repo, product):
        # Arrange
        data = CreateProduct(name="Laptop", sku="LAP-123", price=Decimal("500.00"))
        
        mock_product_repo.create.return_value = product
        
        # Act
        result = product_service.create(data)

        # Assert
        mock_product_repo.create.assert_called_once_with(data)
        assert result.id == 1
        assert result.name == "Laptop"
        assert result.sku == "LAP-123"
        assert result.price == Decimal("500.00")

    def test_create_product_raises_when_sku_exists(self, product_service, mock_product_repo):
        # Arrange
        data = CreateProduct(name="Laptop", sku="DUPLICATE-SKU", price=Decimal("500.00"))
        
        mock_product_repo.create.side_effect = SKUAlreadyExistsError("DUPLICATE-SKU")
        
        # Act and Assert
        with pytest.raises(SKUAlreadyExistsError):
            product_service.create(data)