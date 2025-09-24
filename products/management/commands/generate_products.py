import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from core.models import User
from products.models import (
    Product,
    ProductCategory,
    ProductStatus,
    ProductType,
    ShippingClass,
    TaxClass,
)

fake = Faker()


class Command(BaseCommand):
    help = "Generate sample products"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of products to create")

    def handle(self, *args, **options):
        count = options["count"]
        categories = list(ProductCategory.objects.all())

        admin_user = User.objects.filter(is_superuser=True).first()

        if not categories:
            self.stdout.write(
                self.style.ERROR("No categories found. Please create categories first.")
            )
            return

        for i in range(count):
            name = fake.unique.catch_phrase()
            category = random.choice(categories)
            price = Decimal(str(round(random.uniform(9.99, 999.99), 2)))
            compare_price = (
                price * Decimal("1.2") if random.choice([True, False]) else None
            )
            cost_price = price * Decimal("0.6")

            product = Product.objects.create(
                name=name,
                slug=slugify(name),
                description=fake.paragraph(nb_sentences=5),
                category=category,
                type=random.choice(ProductType.choices)[0],
                tax_class=random.choice(TaxClass.choices)[0],
                shipping_class=random.choice(ShippingClass.choices)[0],
                price=price,
                compare_at_price=compare_price,
                cost_price=cost_price,
                quantity=random.randint(0, 100),
                low_stock_threshold=random.randint(5, 20),
                weight=Decimal(str(round(random.uniform(0.1, 10.0), 2))),
                length=Decimal(str(round(random.uniform(1, 100), 2))),
                width=Decimal(str(round(random.uniform(1, 100), 2))),
                height=Decimal(str(round(random.uniform(1, 100), 2))),
                status=random.choice(ProductStatus.choices)[0],
                featured=random.choice([True, False]),
                seo_title=f"{name} - Buy {name.lower()} at great prices",
                seo_description=fake.text(max_nb_chars=160),
                seo_keywords=f"{name.lower()}, buy {name.lower()}, {category.name.lower()}",
                created_by=admin_user,
            )

            self.stdout.write(
                f"Created product: {product.name} (Category: {category.name})"
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} products"))
