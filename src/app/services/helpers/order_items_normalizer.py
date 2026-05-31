from app.schemas.order import CreateOrderItem


class OrderItemsNormalizer:

    @staticmethod
    def merge_duplicates(
        items: list[CreateOrderItem],
    ) -> list[CreateOrderItem]:

        merged: dict[int, CreateOrderItem] = {}

        for item in items:
            if item.product_id not in merged:
                merged[item.product_id] = CreateOrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                )
            else:
                merged[item.product_id].quantity += item.quantity

        return list(merged.values())