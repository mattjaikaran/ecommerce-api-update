import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from products.models import (
    BundleItem,
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductBundle,
    ProductOption,
    ProductOptionValue,
    ProductTag,
)

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Generate sample product options, attributes, bundles, and tags"

    def add_arguments(self, parser):
        parser.add_argument(
            "--options-count",
            type=int,
            default=5,
            help="Number of product options to create",
        )
        parser.add_argument(
            "--attributes-count",
            type=int,
            default=10,
            help="Number of product attributes to create",
        )
        parser.add_argument(
            "--bundles-count",
            type=int,
            default=5,
            help="Number of product bundles to create",
        )
        parser.add_argument(
            "--tags-count",
            type=int,
            default=15,
            help="Number of product tags to create",
        )

    def handle(self, *args, **options):
        options_count = options["options_count"]
        attributes_count = options["attributes_count"]
        bundles_count = options["bundles_count"]
        tags_count = options["tags_count"]

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(
                self.style.ERROR(
                    "No admin user found. Please create an admin user first."
                )
            )
            return

        products = list(Product.objects.all())
        if not products:
            self.stdout.write(
                self.style.ERROR("No products found. Please create products first.")
            )
            return

        # Generate Product Options
        option_names = [
            "Size",
            "Color",
            "Material",
            "Style",
            "Finish",
            "Pattern",
            "Weight",
            "Length",
            "Width",
            "Height",
        ]
        for i in range(min(options_count, len(option_names))):
            option = ProductOption.objects.create(
                name=option_names[i],
                position=i,
                created_by=admin_user,
            )

            # Generate values for each option
            if option.name == "Size":
                values = ["XS", "S", "M", "L", "XL", "XXL"]
            elif option.name == "Color":
                values = ["Red", "Blue", "Green", "Black", "White", "Yellow"]
            elif option.name == "Material":
                values = ["Cotton", "Polyester", "Wool", "Silk", "Leather"]
            else:
                values = [fake.word() for _ in range(random.randint(3, 6))]

            for j, value in enumerate(values):
                ProductOptionValue.objects.create(
                    option=option,
                    name=value,
                    position=j,
                    created_by=admin_user,
                )

            self.stdout.write(
                f"Created option: {option.name} with {len(values)} values"
            )

        # Generate Product Attributes
        attribute_names = [
            "Brand",
            "Manufacturer",
            "Country of Origin",
            "Care Instructions",
            "Warranty",
            "Certification",
            "Age Group",
            "Gender",
            "Season",
            "Occasion",
        ]
        for i in range(min(attributes_count, len(attribute_names))):
            attribute = ProductAttribute.objects.create(
                name=attribute_names[i],
                code=slugify(attribute_names[i]),
                is_filterable=True,
                position=i,
                created_by=admin_user,
            )

            # Generate values for each attribute
            values = [fake.word() for _ in range(random.randint(3, 8))]
            for j, value in enumerate(values):
                ProductAttributeValue.objects.create(
                    attribute=attribute,
                    value=value,
                    position=j,
                    created_by=admin_user,
                )

            self.stdout.write(
                f"Created attribute: {attribute.name} with {len(values)} values"
            )

        # Generate Product Bundles
        for i in range(bundles_count):
            name = f"{fake.word().title()} Bundle {i + 1}"
            bundle = ProductBundle.objects.create(
                name=name,
                slug=slugify(name),
                description=fake.paragraph(),
                discount_percentage=random.randint(5, 30),
                is_active=True,
                created_by=admin_user,
            )

            # Add random products to bundle
            bundle_products = random.sample(products, random.randint(2, 5))
            for j, product in enumerate(bundle_products):
                BundleItem.objects.create(
                    bundle=bundle,
                    product=product,
                    quantity=random.randint(1, 3),
                    position=j,
                    created_by=admin_user,
                )

            self.stdout.write(
                f"Created bundle: {bundle.name} with {len(bundle_products)} products"
            )

        # Generate Product Tags
        tag_names = [
            "New Arrival",
            "Best Seller",
            "Sale",
            "Featured",
            "Limited Edition",
            "Eco-Friendly",
            "Handmade",
            "Premium",
            "Organic",
            "Sustainable",
            "Vegan",
            "Luxury",
            "Trending",
            "Exclusive",
            "Popular",
        ]
        for i in range(min(tags_count, len(tag_names))):
            name = tag_names[i]
            tag = ProductTag.objects.create(
                name=name,
                slug=slugify(name),
                description=fake.sentence(),
                created_by=admin_user,
            )

            # Add random products to tag
            tag_products = random.sample(products, random.randint(5, 15))
            tag.products.add(*tag_products)

            self.stdout.write(
                f"Created tag: {tag.name} with {len(tag_products)} products"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {options_count} options, {attributes_count} attributes, "
                f"{bundles_count} bundles, and {tags_count} tags"
            )
        )
