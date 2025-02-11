from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
from products.models import Product, ProductReview

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

        for i in range(count):
            product = random.choice(products)
            user = random.choice(users)
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
            )

            self.stdout.write(
                f"Created review: {review.title} ({review.rating} stars) "
                f"for product: {product.name} by user: {user.username}"
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} reviews"))
