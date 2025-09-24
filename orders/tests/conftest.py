import pytest

from .factories import OrderFactory, OrderLineItemFactory


@pytest.fixture
def order(customer):
    """Create an order for a customer."""
    return OrderFactory(customer=customer)


@pytest.fixture
def order_line_item(order, product_variant):
    """Create an order line item."""
    return OrderLineItemFactory(order=order, product_variant=product_variant)
