import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from core.models import Address, Customer

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Generate sample customers with addresses"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of customers to create")
        parser.add_argument(
            "--address-ratio",
            type=float,
            default=0.8,
            help="Ratio of customers that should have addresses (0-1)",
        )

    def handle(self, *args, **options):
        count = options["count"]
        address_ratio = min(max(options["address_ratio"], 0), 1)

        # Get all non-superuser users without customers
        users = User.objects.filter(is_superuser=False, customer__isnull=True)

        if not users:
            self.stdout.write(
                self.style.ERROR("No available users found. Please create users first.")
            )
            return

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(
                self.style.ERROR(
                    "No admin user found. Please create an admin user first."
                )
            )
            return

        created_count = 0
        for user in users:
            if created_count >= count:
                break

            try:
                # Create customer
                customer = Customer.objects.create(
                    user=user,
                    phone=fake.phone_number(),
                    created_by=admin_user,
                )

                # Decide if this customer should have addresses
                if random.random() < address_ratio:
                    # Create 1-3 addresses for the customer
                    num_addresses = random.randint(1, 3)
                    for i in range(num_addresses):
                        is_default = i == 0  # First address is default
                        Address.objects.create(
                            user=user,
                            address_line_1=fake.street_address(),
                            city=fake.city(),
                            state=fake.state(),
                            zip_code=fake.zipcode(),
                            country=fake.country(),
                            phone=fake.phone_number(),
                            is_default=is_default,
                            is_billing=is_default,
                            is_shipping=is_default,
                            is_billing_default=is_default,
                            is_shipping_default=is_default,
                            created_by=admin_user,
                        )

                created_count += 1
                self.stdout.write(
                    f"Created customer for user: {user.email} with {num_addresses if random.random() < address_ratio else 0} addresses"
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating customer for {user.email}: {e}")
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} customers")
        )
