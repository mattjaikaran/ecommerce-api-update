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
from django.contrib.auth import get_user_model

fake = Faker()
User = get_user_model()


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

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(
                self.style.ERROR(
                    "No admin user found. Please create an admin user first."
                )
            )
            return

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
            if random.random() < status_ratio:
                # Create fulfillment order
                fulfillment = FulfillmentOrder.objects.create(
                    order=order,
                    status=random.choice(FulfillmentStatus.choices)[0],
                    tracking_number=fake.uuid4(),
                    tracking_url=f"https://tracking.example.com/{fake.uuid4()}",
                    created_by=admin_user,
                )

                # Create fulfillment line items for each order item
                for order_item in order.items.all():
                    FulfillmentLineItem.objects.create(
                        fulfillment=fulfillment,
                        order_line_item=order_item,
                        quantity=order_item.quantity,
                        created_by=admin_user,
                    )

                fulfilled_count += 1
                self.stdout.write(
                    f"Created fulfillment for order {order.order_number} with status {fulfillment.status}"
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {fulfilled_count} fulfillments")
        )
