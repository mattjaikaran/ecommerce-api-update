from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
import random
from products.models import Product, ProductCollection
from django.contrib.auth import get_user_model

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Generate sample product collections"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of collections to create")
        parser.add_argument(
            "--min-products",
            type=int,
            default=5,
            help="Minimum products per collection",
        )
        parser.add_argument(
            "--max-products",
            type=int,
            default=20,
            help="Maximum products per collection",
        )

    def handle(self, *args, **options):
        count = options["count"]
        min_products = options["min_products"]
        max_products = options["max_products"]
        products = list(Product.objects.all())

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(
                self.style.ERROR(
                    "No admin user found. Please create an admin user first."
                )
            )
            return

        if not products:
            self.stdout.write(
                self.style.ERROR("No products found. Please create products first.")
            )
            return

        for i in range(count):
            name = fake.unique.catch_phrase()
            collection = ProductCollection.objects.create(
                name=name,
                slug=slugify(name),
                description=fake.paragraph(),
                is_active=True,
                position=i,
                seo_title=f"{name} Collection - Shop {name.lower()}",
                seo_description=fake.text(max_nb_chars=160),
                seo_keywords=f"{name.lower()}, collection, shop {name.lower()}",
                created_by=admin_user,
            )

            # Add random products to collection
            product_count = random.randint(
                min_products, min(max_products, len(products))
            )
            collection_products = random.sample(products, product_count)
            collection.products.add(*collection_products)

            self.stdout.write(
                f"Created collection: {collection.name} with {product_count} products"
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} collections")
        )
