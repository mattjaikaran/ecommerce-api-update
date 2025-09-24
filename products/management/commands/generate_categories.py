from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from products.models import ProductCategory

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Generate sample product categories"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of categories to create")
        parser.add_argument(
            "--parent-count", type=int, default=5, help="Number of parent categories"
        )

    def handle(self, *args, **options):
        count = options["count"]
        parent_count = min(options["parent_count"], count)

        # Get or create a superuser for the created_by field
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                self.stdout.write(
                    self.style.ERROR(
                        "No superuser found. Please create a superuser first using: python manage.py createsuperuser"
                    )
                )
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error getting superuser: {e}"))
            return

        # Create parent categories
        parent_categories = []
        for i in range(parent_count):
            name = fake.unique.company()
            category = ProductCategory.objects.create(
                name=name,
                slug=slugify(name),
                description=fake.paragraph(),
                seo_title=f"{name} - Shop the best {name.lower()}",
                seo_description=fake.text(max_nb_chars=160),
                seo_keywords=f"{name.lower()}, shop {name.lower()}, buy {name.lower()}",
                position=i,
                created_by=admin_user,
                updated_by=admin_user,
            )
            parent_categories.append(category)
            self.stdout.write(f"Created parent category: {category.name}")

        # Create child categories
        remaining = count - parent_count
        if remaining > 0:
            for i in range(remaining):
                name = fake.unique.catch_phrase()
                parent = fake.random_element(parent_categories)
                category = ProductCategory.objects.create(
                    name=name,
                    slug=slugify(name),
                    description=fake.paragraph(),
                    parent=parent,
                    seo_title=f"{name} - Shop {parent.name} {name.lower()}",
                    seo_description=fake.text(max_nb_chars=160),
                    seo_keywords=f"{name.lower()}, {parent.name.lower()}, shop {name.lower()}",
                    position=i,
                    created_by=admin_user,
                    updated_by=admin_user,
                )
                self.stdout.write(
                    f"Created child category: {category.name} (Parent: {parent.name})"
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} categories")
        )
