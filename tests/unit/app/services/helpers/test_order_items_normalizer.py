import pytest
from pydantic import ValidationError

from app.services.helpers import OrderItemsNormalizer
from app.schemas.order import CreateOrderItem


class TestOrderItemsNormalizer:

    def test_merge_duplicates_non_contiguous(self):
        items = [
            CreateOrderItem(product_id=1, quantity=2),
            CreateOrderItem(product_id=2, quantity=1),
            CreateOrderItem(product_id=1, quantity=3),
            CreateOrderItem(product_id=3, quantity=5),
            CreateOrderItem(product_id=2, quantity=4),
            CreateOrderItem(product_id=1, quantity=1),
        ]

        result = OrderItemsNormalizer.merge_duplicates(items)

        assert len(result) == 3

        result_map = {i.product_id: i.quantity for i in result}

        assert result_map[1] == 6
        assert result_map[2] == 5
        assert result_map[3] == 5

    def test_merge_duplicates_does_not_mutate_input(self):
        item1 = CreateOrderItem(product_id=1, quantity=2)
        item2 = CreateOrderItem(product_id=1, quantity=3)

        items = [item1, item2]
        original = [(i.product_id, i.quantity) for i in items]

        OrderItemsNormalizer.merge_duplicates(items)

        assert [(i.product_id, i.quantity) for i in items] == original

    def test_merge_duplicates_returns_correct_totals(self):
        items = [
            CreateOrderItem(product_id=i % 3, quantity=1)
            for i in range(30)
        ]

        result = OrderItemsNormalizer.merge_duplicates(items)

        assert len(result) == 3

        total_map = {i.product_id: i.quantity for i in result}

        assert total_map[0] == 10
        assert total_map[1] == 10
        assert total_map[2] == 10

    def test_schema_validation_rules_still_apply(self):
        with pytest.raises(ValidationError):
            CreateOrderItem(product_id=1, quantity=0)

        with pytest.raises(ValidationError):
            CreateOrderItem(product_id=1, quantity=-1)