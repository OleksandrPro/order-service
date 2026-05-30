from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import List
from decimal import Decimal


class CreateOrderItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CreateOrder(BaseModel):
    customer_id: int
    items: List[CreateOrderItem]

    @model_validator(mode="after")
    def validate_items(self):
        if not self.items:
            raise ValueError("Order must contain at least one item")
        return self

class OrderItemSnapshot(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: Decimal


class OrderSnapshot(BaseModel):
    customer_id: int
    items: list[OrderItemSnapshot]
    total_amount: Decimal

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

    model_config = ConfigDict(from_attributes=True)


class Order(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    items: list[OrderItem]

    model_config = ConfigDict(from_attributes=True)