from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


class CreateProduct(BaseModel):
    name: str
    sku: str = Field(min_length=5, max_length=50)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0, default=0)


class Product(BaseModel):
    id: int
    name: str
    sku: str
    price: Decimal
    stock: int

    model_config = ConfigDict(from_attributes=True)