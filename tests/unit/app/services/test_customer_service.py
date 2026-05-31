import pytest
from datetime import datetime
from app.schemas.customer import CreateCustomer, Customer
from app.exceptions.domain import EmailAlreadyTakenError
from app.services.customer_service import CustomerService

class TestCustomerService:

    def test_create_customer_success(self, mock_customer_repo):
        # Arrange
        data = CreateCustomer(name="John Doe", email="john@example.com")
        
        expected_customer = Customer(
            id=1, 
            name="John Doe", 
            email="john@example.com",
            created_at=datetime.now()
        )
        mock_customer_repo.create.return_value = expected_customer
        
        service = CustomerService(mock_customer_repo)

        # Act
        result = service.create(data)

        # Assert
        mock_customer_repo.create.assert_called_once_with(data)
        assert result.id == 1
        assert result.name == "John Doe"
        assert result.email == "john@example.com"

    def test_create_customer_raises_when_email_taken(self, mock_customer_repo):
        # Arrange
        data = CreateCustomer(name="John Doe", email="taken@example.com")
        
        mock_customer_repo.create.side_effect = EmailAlreadyTakenError("taken@example.com")
        
        service = CustomerService(mock_customer_repo)

        # Act and Assert
        with pytest.raises(EmailAlreadyTakenError):
            service.create(data)