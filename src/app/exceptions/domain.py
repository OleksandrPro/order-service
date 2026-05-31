from .base import OrderServiceError

class CustomerCreationError(OrderServiceError):
    def __init__(self):
        super().__init__(f"Error while creating a new customer")

class CustomerNotFoundError(OrderServiceError):
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        super().__init__(f"Customer with id '{customer_id}' doesn't exist")

class EmailAlreadyTakenError(OrderServiceError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email '{email}' has already been used")

class ProductNotFoundError(OrderServiceError):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with id '{product_id}' doesn't exist")
        
class SKUAlreadyExistsError(OrderServiceError):
    def __init__(self, sku: str):
        self.sku = sku
        super().__init__(f"SKU '{sku}' already exists")