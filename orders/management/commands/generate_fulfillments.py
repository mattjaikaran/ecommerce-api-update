from django.core.management.base import BaseCommand
from faker import Faker
import random
from orders.models import (
    Order,
    OrderStatus,
    FulfillmentOrder,
    FulfillmentLineItem,
    FulfillmentStatus,
)

fake = Faker()


class Command(BaseCommand):
    help = "Generate fulfillments for paid orders"

    def add_arguments(self, parser):
        parser.add_argument(
            "--status-ratio",
            type=float,
            default=0.7,
            help="Ratio of orders to fulfill (0-1)",
        )

    def handle(self, *args, **options):
        status_ratio = min(max(options["status_ratio"], 0), 1)

        # Get paid orders without fulfillments
        orders = Order.objects.filter(
            status=OrderStatus.PAID, fulfillments__isnull=True
        )

        if not orders:
            self.stdout.write(
                self.style.ERROR("No paid orders found without fulfillments.")
            )
            return

        fulfilled_count = 0
        for order in orders:
            # Randomly decide if we should fulfill this order
            if random.random() > status_ratio:
                continue

            # Create fulfillment order
            fulfillment = FulfillmentOrder.objects.create(
                order=order,
                status=random.choice(FulfillmentStatus.choices)[0],
                shipping_method=order.shipping_method,
                shipping_carrier=random.choice(["FedEx", "UPS", "USPS", "DHL"]),
                tracking_number=fake.uuid4(),
                tracking_url=f"https://track.carrier.com/{fake.uuid4()}",
                shipping_label_url=f"https://shipping.carrier.com/labels/{fake.uuid4()}.pdf",
                notes=(
                    fake.text(max_nb_chars=200)
                    if random.choice([True, False])
                    else None
                ),
            )

            # Create fulfillment line items for all order items
            for order_item in order.items.all():
                FulfillmentLineItem.objects.create(
                    fulfillment=fulfillment,
                    order_item=order_item,
                    quantity=order_item.quantity,
                )

            # Update order status
            order.status = OrderStatus.SHIPPED
            order.save()

            fulfilled_count += 1
            self.stdout.write(
                f"Created fulfillment for order {order.order_number} "
                f"with carrier {fulfillment.shipping_carrier}"
            )

        if fulfilled_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {fulfilled_count} fulfillments"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING("No orders were fulfilled based on the given ratio.")
            )
