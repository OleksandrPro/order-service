import pytest
from app.schemas.order import CreateOrderItem
from app.services.helpers import OrderItemsNormalizer
from pydantic import ValidationError

class TestOrderItemsNormalizer:

    def test_merge_duplicates_does_not_mutate_input(self):
        # Arrange
        original_item = CreateOrderItem(product_id=1, quantity=2)
        items = [original_item, CreateOrderItem(product_id=1, quantity=3)]
        
        # Act
        result = OrderItemsNormalizer.merge_duplicates(items)
        
        # Assert
        assert original_item.quantity == 2
        assert items[0].quantity == 2
        assert len(items) == 2

    def test_merge_duplicates_non_contiguous(self):
        # Arrange
        items = [
            CreateOrderItem(product_id=1, quantity=2),
            CreateOrderItem(product_id=2, quantity=1),
            CreateOrderItem(product_id=1, quantity=3),
            CreateOrderItem(product_id=3, quantity=5),
            CreateOrderItem(product_id=2, quantity=4),
            CreateOrderItem(product_id=1, quantity=1),
        ]
        
        # Act
        result = OrderItemsNormalizer.merge_duplicates(items)
        
        # Assert
        assert len(result) == 3
        assert result[0].product_id == 1
        assert result[0].quantity == 6
        assert result[1].product_id == 2
        assert result[1].quantity == 5
        assert result[2].product_id == 3
        assert result[2].quantity == 5

    def test_merge_duplicates_large_input(self):
        # Arrange
        items = [
            CreateOrderItem(product_id=i % 10, quantity=1) 
            for i in range(10000)
        ]
        
        # Act
        result = OrderItemsNormalizer.merge_duplicates(items)
        
        # Assert
        assert len(result) == 10
        for item in result:
            assert item.quantity == 1000

    def test_single_item_returns_same_value_not_new_object(self):
        # Arrange
        item = CreateOrderItem(product_id=1, quantity=5)
        items = [item]
        
        # Act
        result = OrderItemsNormalizer.merge_duplicates(items)
        
        # Assert
        assert len(result) == 1
        assert result[0].product_id == 1
        assert result[0].quantity == 5

    def test_schema_blocks_zero_and_negative_quantity(self):
        # Act and Assert
        with pytest.raises(ValidationError):
            CreateOrderItem(product_id=1, quantity=0)
            
        with pytest.raises(ValidationError):
            CreateOrderItem(product_id=1, quantity=-2)