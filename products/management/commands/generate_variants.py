from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from decimal import Decimal
import random
from products.models import Product, ProductVariant
from core.models import User
from django.db import IntegrityError

fake = Faker()


class Command(BaseCommand):
    help = "Generate sample product variants"

    def add_arguments(self, parser):
        parser.add_argument(
            "--min-variants", type=int, default=2, help="Minimum variants per product"
        )
        parser.add_argument(
            "--max-variants", type=int, default=5, help="Maximum variants per product"
        )

    def handle(self, *args, **options):
        min_variants = options["min_variants"]
        max_variants = options["max_variants"]
        products = Product.objects.all()

        admin_user = User.objects.filter(is_superuser=True).first()

        if not products:
            self.stdout.write(
                self.style.ERROR("No products found. Please create products first.")
            )
            return

        total_variants = 0
        for product in products:
            # Skip if product already has variants
            if product.variants.exists():
                continue

            variant_count = random.randint(min_variants, max_variants)
            base_price = product.price

            for i in range(variant_count):
                # Keep trying until we get a unique SKU
                attempt = 0
                while True:
                    try:
                        # Generate variant name based on attributes (size, color, etc.)
                        variant_name = f"{product.name} - Variant {i+1}"
                        # Add attempt number to SKU if we've tried before
                        sku_suffix = f"-{attempt}" if attempt > 0 else ""
                        sku = f"{slugify(product.name)[:10]}-V{i+1}{sku_suffix}"

                        # Adjust price slightly from base price
                        price_adjustment = Decimal(
                            str(round(random.uniform(-20, 20), 2))
                        )
                        variant_price = max(
                            base_price + price_adjustment, Decimal("0.01")
                        )

                        variant = ProductVariant.objects.create(
                            product=product,
                            name=variant_name,
                            sku=sku,
                            barcode=fake.ean13(),
                            price=variant_price,
                            compare_at_price=(
                                variant_price * Decimal("1.2")
                                if random.choice([True, False])
                                else None
                            ),
                            cost_price=variant_price * Decimal("0.6"),
                            inventory_quantity=random.randint(0, 100),
                            low_stock_threshold=random.randint(5, 20),
                            weight=product.weight
                            + Decimal(str(round(random.uniform(-0.5, 0.5), 2))),
                            length=product.length
                            + Decimal(str(round(random.uniform(-5, 5), 2))),
                            width=product.width
                            + Decimal(str(round(random.uniform(-5, 5), 2))),
                            height=product.height
                            + Decimal(str(round(random.uniform(-5, 5), 2))),
                            position=i,
                            is_active=True,
                            created_by=admin_user,
                            is_deleted=False,
                            deleted_at=None,
                        )
                        total_variants += 1
                        self.stdout.write(
                            f"Created variant: {variant.name} (SKU: {sku}) for product: {product.name}"
                        )
                        break  # Break the while loop if successful
                    except IntegrityError as e:
                        if "sku" in str(e):
                            # If SKU already exists, increment attempt and try again
                            attempt += 1
                            continue
                        else:
                            # If it's some other integrity error, raise it
                            raise e

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {total_variants} variants")
        )
