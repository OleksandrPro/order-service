import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_customer_repo():
    repo = MagicMock()
    return repo

@pytest.fixture
def mock_product_repo():
    return MagicMock()

@pytest.fixture
def mock_order_repo():
    return MagicMock()