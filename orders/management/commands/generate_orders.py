from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from decimal import Decimal
import random
from orders.models import (
    Order,
    OrderLineItem,
    OrderStatus,
    PaymentStatus,
    PaymentMethod,
    ShippingMethod,
)
from products.models import ProductVariant
from core.models import Customer, Address, CustomerGroup
from django.contrib.auth import get_user_model

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Generate sample orders"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of orders to create")
        parser.add_argument(
            "--min-items", type=int, default=1, help="Minimum items per order"
        )
        parser.add_argument(
            "--max-items", type=int, default=5, help="Maximum items per order"
        )

    def handle(self, *args, **options):
        count = options["count"]
        min_items = options["min_items"]
        max_items = options["max_items"]

        customers = list(Customer.objects.all())
        variants = list(ProductVariant.objects.filter(is_active=True))
        customer_groups = list(CustomerGroup.objects.all())

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(
                self.style.ERROR(
                    "No admin user found. Please create an admin user first."
                )
            )
            return

        if not customers:
            self.stdout.write(
                self.style.ERROR("No customers found. Please create customers first.")
            )
            return

        if not variants:
            self.stdout.write(
                self.style.ERROR(
                    "No product variants found. Please create products and variants first."
                )
            )
            return

        for i in range(count):
            customer = random.choice(customers)
            customer_group = random.choice(customer_groups) if customer_groups else None

            # Get or create addresses
            addresses = Address.objects.filter(user=customer.user)
            if not addresses.exists():
                billing_address = shipping_address = Address.objects.create(
                    user=customer.user,
                    address_line_1=fake.street_address(),
                    city=fake.city(),
                    state=fake.state(),
                    zip_code=fake.zipcode(),
                    country=fake.country(),
                    phone=fake.phone_number(),
                    is_default=True,
                    created_by=admin_user,
                )
            else:
                billing_address = shipping_address = random.choice(addresses)

            # Create order
            order_number = f"ORD-{timezone.now().strftime('%Y%m%d')}-{fake.random_int(min=1000, max=9999)}"
            status = random.choice(OrderStatus.choices)[0]
            payment_status = random.choice(PaymentStatus.choices)[0]
            payment_method = random.choice(PaymentMethod.choices)[0]
            shipping_method = random.choice(ShippingMethod.choices)[0]

            order = Order.objects.create(
                customer=customer,
                customer_group=customer_group,
                order_number=order_number,
                status=status,
                currency="USD",
                subtotal=Decimal("0.00"),
                shipping_amount=Decimal("0.00"),
                shipping_method=shipping_method,
                shipping_tax_amount=Decimal("0.00"),
                tax_amount=Decimal("0.00"),
                discount_amount=Decimal("0.00"),
                total=Decimal("0.00"),
                payment_status=payment_status,
                payment_method=payment_method,
                payment_gateway="stripe",
                billing_address=billing_address,
                shipping_address=shipping_address,
                email=customer.user.email,
                phone=customer.phone,
                ip_address=fake.ipv4(),
                user_agent=fake.user_agent(),
                meta_data={},
                created_by=admin_user,
            )

            # Add random items to order
            item_count = random.randint(min_items, max_items)
            order_variants = random.sample(variants, item_count)

            subtotal = Decimal("0.00")
            for variant in order_variants:
                quantity = random.randint(1, 3)
                unit_price = variant.price
                line_subtotal = unit_price * quantity
                tax_rate = Decimal("0.08")  # 8% tax rate
                tax_amount = line_subtotal * tax_rate

                OrderLineItem.objects.create(
                    order=order,
                    product_variant=variant,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=line_subtotal,
                    tax_rate=tax_rate,
                    tax_amount=tax_amount,
                    total=line_subtotal + tax_amount,
                    weight=(
                        variant.weight * quantity if variant.weight else Decimal("0.00")
                    ),
                    created_by=admin_user,
                )

                subtotal += line_subtotal

            # Calculate order totals
            shipping_amount = (
                Decimal("9.99")
                if shipping_method != ShippingMethod.FREE
                else Decimal("0.00")
            )
            shipping_tax_amount = shipping_amount * Decimal(
                "0.08"
            )  # 8% tax on shipping
            tax_amount = sum(item.tax_amount for item in order.items.all())
            total = subtotal + shipping_amount + shipping_tax_amount + tax_amount

            # Update order with totals
            order.subtotal = subtotal
            order.shipping_amount = shipping_amount
            order.shipping_tax_amount = shipping_tax_amount
            order.tax_amount = tax_amount
            order.total = total
            order.save()

            self.stdout.write(
                f"Created order {order.order_number} for {customer.user.email} "
                f"with {item_count} items. Status: {status}, Total: ${total}"
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} orders"))
