from pydantic import BaseModel, ConfigDict, Field, field_validator
from decimal import Decimal


class CreateProduct(BaseModel):
    name: str
    sku: str = Field(min_length=5, max_length=50)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0, default=0)

    @field_validator("price")
    @classmethod
    def validate_price_scale(cls, v: Decimal):
        if v.as_tuple().exponent < -2:
            raise ValueError("Price cannot have more than 2 decimal places")
        return v

class ProductStockUpdate(BaseModel):
    product_id: int
    stock: int

class Product(BaseModel):
    id: int
    name: str
    sku: str
    price: Decimal
    stock: int

    model_config = ConfigDict(from_attributes=True)