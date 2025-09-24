"""Factory for Address model."""

import factory

from core.models import Address

from .user_factory import UserFactory


class AddressFactory(factory.django.DjangoModelFactory):
    """Factory for creating Address instances."""

    class Meta:
        model = Address

    user = factory.SubFactory(UserFactory)
    address_line_1 = factory.Faker("street_address")
    address_line_2 = factory.Faker("secondary_address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    zip_code = factory.Faker("zipcode")
    country = factory.Faker("country")
    phone = factory.Faker("phone_number")
    is_default = False
    is_billing = False
    is_shipping = False
    is_shipping_default = False
    is_billing_default = False
    created_by = factory.SelfAttribute("user")
    updated_by = factory.SelfAttribute("user")


class BillingAddressFactory(AddressFactory):
    """Factory for creating billing Address instances."""

    is_billing = True
    is_billing_default = True


class ShippingAddressFactory(AddressFactory):
    """Factory for creating shipping Address instances."""

    is_shipping = True
    is_shipping_default = True


class DefaultAddressFactory(AddressFactory):
    """Factory for creating default Address instances."""

    is_default = True
    is_billing = True
    is_shipping = True
    is_billing_default = True
    is_shipping_default = True
