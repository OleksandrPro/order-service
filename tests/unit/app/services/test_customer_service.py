import pytest
from app.schemas.customer import CreateCustomer
from app.exceptions.domain import EmailAlreadyTakenError

class TestCustomerService:

    def test_create_customer_success(self, customer_service, mock_customer_repo, customer):
        # Arrange
        data = CreateCustomer(name="John Doe", email="john@example.com")
        
        mock_customer_repo.create.return_value = customer
        
        # Act
        result = customer_service.create(data)

        # Assert
        mock_customer_repo.create.assert_called_once_with(data)
        assert result.id == 1
        assert result.name == "John Doe"
        assert result.email == "john@example.com"

    def test_create_customer_raises_when_email_taken(self, customer_service, mock_customer_repo):
        # Arrange
        data = CreateCustomer(name="John Doe", email="taken@example.com")
        
        mock_customer_repo.create.side_effect = EmailAlreadyTakenError("taken@example.com")
        
        # Act and Assert
        with pytest.raises(EmailAlreadyTakenError) as exc_info:
            customer_service.create(data)
        
        assert exc_info.value.email == "taken@example.com"