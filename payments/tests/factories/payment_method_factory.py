import factory

from core.tests.factories import UserFactory
from payments.models import PaymentMethod


class PaymentMethodFactory(factory.django.DjangoModelFactory):
    """Factory for creating PaymentMethod instances."""

    class Meta:
        model = PaymentMethod

    name = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=200)
    credentials = factory.LazyFunction(dict)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SelfAttribute("created_by")


class StripePaymentMethodFactory(PaymentMethodFactory):
    """Factory for creating Stripe PaymentMethod instances."""

    name = "Stripe"
    description = "Stripe payment gateway"
    credentials = factory.LazyFunction(
        lambda: {
            "publishable_key": "pk_test_example",
            "secret_key": "sk_test_example",
            "webhook_secret": "whsec_example",
        }
    )


class PayPalPaymentMethodFactory(PaymentMethodFactory):
    """Factory for creating PayPal PaymentMethod instances."""

    name = "PayPal"
    description = "PayPal payment gateway"
    credentials = factory.LazyFunction(
        lambda: {
            "client_id": "example_client_id",
            "client_secret": "example_client_secret",
            "mode": "sandbox",
        }
    )
