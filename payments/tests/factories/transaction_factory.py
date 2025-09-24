from decimal import Decimal

import factory

from orders.tests.factories import OrderFactory
from payments.models import Transaction

from .payment_method_factory import PaymentMethodFactory


class TransactionFactory(factory.django.DjangoModelFactory):
    """Factory for creating Transaction instances."""

    class Meta:
        model = Transaction

    order = factory.SubFactory(OrderFactory)
    amount = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=2,
        positive=True,
        min_value=Decimal("1.00"),
        max_value=Decimal("999.99"),
    )
    status = "completed"
    notes = factory.Faker("text", max_nb_chars=200)
    payment_method = factory.SubFactory(PaymentMethodFactory)
    transaction_id = factory.Faker("uuid4")
    transaction_type = "payment"
    transaction_status = "completed"
    transaction_response = factory.LazyFunction(dict)
    transaction_currency = "USD"
    transaction_amount = factory.SelfAttribute("amount")
    transaction_fee = factory.Faker(
        "pydecimal",
        left_digits=1,
        right_digits=2,
        positive=True,
        min_value=Decimal("0.30"),
        max_value=Decimal("5.00"),
    )
    transaction_tax = factory.Faker(
        "pydecimal",
        left_digits=1,
        right_digits=2,
        positive=True,
        min_value=Decimal("0.00"),
        max_value=Decimal("10.00"),
    )
    transaction_total = factory.LazyAttribute(
        lambda obj: obj.transaction_amount + obj.transaction_fee + obj.transaction_tax
    )
    created_by = factory.SelfAttribute("order.customer.user")
    updated_by = factory.SelfAttribute("order.customer.user")


class SuccessfulTransactionFactory(TransactionFactory):
    """Factory for creating successful Transaction instances."""

    status = "completed"
    transaction_status = "completed"


class FailedTransactionFactory(TransactionFactory):
    """Factory for creating failed Transaction instances."""

    status = "failed"
    transaction_status = "failed"


class PendingTransactionFactory(TransactionFactory):
    """Factory for creating pending Transaction instances."""

    status = "pending"
    transaction_status = "pending"
