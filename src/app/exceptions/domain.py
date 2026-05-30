from .base import OrderServiceError

class CustomerCreationError(OrderServiceError):
    def __init__(self):
        super().__init__(f"Error while creating a new customer")

class EmailAlreadyTakenError(OrderServiceError):
    def __init__(self, email: str):
        super().__init__(f"Email '{email}' has already been used")