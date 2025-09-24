import pytest

from .factories import PaymentMethodFactory, TransactionFactory


@pytest.fixture
def payment_method():
    """Create a payment method."""
    return PaymentMethodFactory()


@pytest.fixture
def transaction(order, payment_method):
    """Create a transaction."""
    return TransactionFactory(order=order, payment_method=payment_method)
