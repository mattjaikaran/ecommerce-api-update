import pytest

from .factories import CartFactory, CartItemFactory


@pytest.fixture
def cart(customer):
    """Create a cart for a customer."""
    return CartFactory(customer=customer)


@pytest.fixture
def cart_item(cart, product_variant):
    """Create a cart item."""
    return CartItemFactory(cart=cart, product_variant=product_variant)
