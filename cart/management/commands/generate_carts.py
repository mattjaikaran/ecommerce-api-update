from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import timedelta
import random
from cart.models import Cart, CartItem
from products.models import ProductVariant
from core.models import Customer
from django.contrib.auth import get_user_model

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Generate sample shopping carts"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of carts to create")
        parser.add_argument(
            "--min-items", type=int, default=1, help="Minimum items per cart"
        )
        parser.add_argument(
            "--max-items", type=int, default=5, help="Maximum items per cart"
        )
        parser.add_argument(
            "--abandoned-ratio",
            type=float,
            default=0.3,
            help="Ratio of abandoned carts (0-1)",
        )

    def handle(self, *args, **options):
        count = options["count"]
        min_items = options["min_items"]
        max_items = options["max_items"]
        abandoned_ratio = min(max(options["abandoned_ratio"], 0), 1)

        customers = list(Customer.objects.all())
        variants = list(ProductVariant.objects.filter(is_active=True))

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
            # Randomly decide if this cart should be abandoned
            is_abandoned = random.random() < abandoned_ratio
            customer = random.choice(customers)

            cart = Cart.objects.create(
                customer=customer,
                session_key=fake.uuid4() if is_abandoned else None,
                expires_at=(
                    timezone.now() + timedelta(days=random.randint(1, 30))
                    if is_abandoned
                    else None
                ),
                is_active=not is_abandoned,
                created_by=admin_user,
            )

            # Add random items to cart
            item_count = random.randint(min_items, max_items)
            cart_variants = random.sample(variants, item_count)

            subtotal = 0
            total_quantity = 0

            for variant in cart_variants:
                quantity = random.randint(1, 3)
                price = variant.price

                CartItem.objects.create(
                    cart=cart,
                    product_variant=variant,
                    quantity=quantity,
                    price=price,
                    created_by=admin_user,
                )

                subtotal += price * quantity
                total_quantity += quantity

            # Update cart totals
            cart.subtotal = subtotal
            cart.total_price = subtotal  # In a real app, you'd add shipping, tax, etc.
            cart.total_quantity = total_quantity
            cart.save()

            status = "Abandoned" if is_abandoned else "Active"
            self.stdout.write(
                f"Created {status} cart for {customer.user.email} with {item_count} items. "
                f"Total: ${cart.total_price}"
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} carts"))
