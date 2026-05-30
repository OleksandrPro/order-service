from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class CreateCustomer(BaseModel):
    name: str
    email: EmailStr

class Customer(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)