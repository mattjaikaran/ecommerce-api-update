"""Factory for Customer and CustomerGroup models."""

import factory

from core.models import Customer, CustomerGroup

from .user_factory import UserFactory


class CustomerFactory(factory.django.DjangoModelFactory):
    """Factory for creating Customer instances."""

    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory)
    phone = factory.Faker("phone_number")
    is_default = False
    created_by = factory.SelfAttribute("user")
    updated_by = factory.SelfAttribute("user")


class CustomerGroupFactory(factory.django.DjangoModelFactory):
    """Factory for creating CustomerGroup instances."""

    class Meta:
        model = CustomerGroup

    name = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=200)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SelfAttribute("created_by")

    @factory.post_generation
    def customers(self, create, extracted, **kwargs):
        """Add customers to the group after creation."""
        if not create:
            return

        if extracted:
            for customer in extracted:
                self.customers.add(customer)
