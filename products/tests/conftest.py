import pytest

from .factories import (
    ProductCategoryFactory,
    ProductFactory,
    ProductVariantFactory,
    PublishedProductFactory,
)


@pytest.fixture
def product_category():
    """Create a product category."""
    return ProductCategoryFactory()


@pytest.fixture
def product(product_category):
    """Create a product."""
    return ProductFactory(category=product_category)


@pytest.fixture
def published_product(product_category):
    """Create a published product."""
    return PublishedProductFactory(category=product_category)


@pytest.fixture
def product_variant(product):
    """Create a product variant."""
    return ProductVariantFactory(product=product)
