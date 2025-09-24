import factory

from cart.models import CartItem
from products.tests.factories import ProductVariantFactory

from .cart_factory import CartFactory


class CartItemFactory(factory.django.DjangoModelFactory):
    """Factory for creating CartItem instances."""

    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product_variant = factory.SubFactory(ProductVariantFactory)
    quantity = factory.Faker("random_int", min=1, max=5)
    price = factory.LazyAttribute(lambda obj: obj.product_variant.price)
    created_by = factory.SelfAttribute("cart.customer.user")
    updated_by = factory.SelfAttribute("cart.customer.user")


class SingleItemFactory(CartItemFactory):
    """Factory for creating single quantity CartItem instances."""

    quantity = 1


class MultipleItemFactory(CartItemFactory):
    """Factory for creating multiple quantity CartItem instances."""

    quantity = factory.Faker("random_int", min=2, max=10)
