from .base import OrderServiceError

class CustomerCreationError(OrderServiceError):
    def __init__(self):
        super().__init__(f"Error while creating a new customer")

class CustomerNotFoundError(OrderServiceError):
    def __init__(self, id: int):
        super().__init__(f"Customer with id '{id}' doesn't exist")

class EmailAlreadyTakenError(OrderServiceError):
    def __init__(self, email: str):
        super().__init__(f"Email '{email}' has already been used")

class ProductNotFoundError(OrderServiceError):
    def __init__(self, id: int):
        super().__init__(f"Product with id '{id}' doesn't exist")
        
class SKUAlreadyExistsError(OrderServiceError):
    def __init__(self, sku: str):
        super().__init__(f"SKU '{sku}' already exists")