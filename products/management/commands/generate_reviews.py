from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
from products.models import Product, ProductReview
from django.db import IntegrityError

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Generate sample product reviews"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of reviews to create")
        parser.add_argument(
            "--verified-ratio",
            type=float,
            default=0.7,
            help="Ratio of verified reviews (0-1)",
        )
        parser.add_argument(
            "--featured-ratio",
            type=float,
            default=0.2,
            help="Ratio of featured reviews (0-1)",
        )

    def handle(self, *args, **options):
        count = options["count"]
        verified_ratio = min(max(options["verified_ratio"], 0), 1)
        featured_ratio = min(max(options["featured_ratio"], 0), 1)

        admin_user = User.objects.filter(is_superuser=True).first()

        if not admin_user:
            self.stdout.write(
                self.style.ERROR(
                    "No admin user found. Please create an admin user first."
                )
            )
            return

        products = list(Product.objects.all())
        users = list(User.objects.all())

        if not products:
            self.stdout.write(
                self.style.ERROR("No products found. Please create products first.")
            )
            return

        if not users:
            self.stdout.write(
                self.style.ERROR("No users found. Please create users first.")
            )
            return

        # Keep track of how many reviews we've successfully created
        created_reviews = 0
        # Keep track of product-user combinations we've tried
        attempted_combinations = set()
        # Maximum number of attempts to avoid infinite loops
        max_attempts = count * 3

        attempts = 0
        while created_reviews < count and attempts < max_attempts:
            product = random.choice(products)
            user = random.choice(users)

            # Skip if we've already tried this combination
            combination = (str(product.id), str(user.id))
            if combination in attempted_combinations:
                attempts += 1
                continue

            attempted_combinations.add(combination)

            try:
                rating = random.randint(1, 5)
                is_verified = random.random() < verified_ratio
                is_featured = random.random() < featured_ratio

                # Generate review title based on rating
                if rating >= 4:
                    title = random.choice(
                        [
                            "Great product!",
                            "Highly recommend",
                            "Excellent quality",
                            "Very satisfied",
                            "Love it!",
                        ]
                    )
                elif rating == 3:
                    title = random.choice(
                        [
                            "Decent product",
                            "Good but not great",
                            "Average quality",
                            "Met expectations",
                            "Room for improvement",
                        ]
                    )
                else:
                    title = random.choice(
                        [
                            "Disappointed",
                            "Not worth the price",
                            "Poor quality",
                            "Would not recommend",
                            "Needs improvement",
                        ]
                    )

                review = ProductReview.objects.create(
                    product=product,
                    user=user,
                    rating=rating,
                    title=title,
                    comment=fake.paragraph(nb_sentences=random.randint(2, 5)),
                    is_verified=is_verified,
                    is_featured=is_featured,
                    created_by=admin_user,
                    is_deleted=False,
                    deleted_at=None,
                )

                created_reviews += 1
                self.stdout.write(
                    f"Created review {created_reviews}/{count}: {review.title} ({review.rating} stars) "
                    f"for product: {product.name} by user: {user.username}"
                )

            except IntegrityError:
                # Skip this combination if it already exists
                attempts += 1
                continue

        if created_reviews < count:
            self.stdout.write(
                self.style.WARNING(
                    f"Only created {created_reviews} reviews out of {count} requested. "
                    "This may be because there weren't enough unique product-user combinations available."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created {created_reviews} reviews")
            )
