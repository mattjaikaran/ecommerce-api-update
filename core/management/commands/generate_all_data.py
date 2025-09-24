"""Generate all test data for the ecommerce platform."""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Generate comprehensive test data for all apps."""

    help = "Generate comprehensive test data for all apps in the ecommerce platform"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--quick",
            action="store_true",
            help="Generate minimal test data for quick setup",
        )
        parser.add_argument(
            "--full",
            action="store_true",
            help="Generate comprehensive test data (default)",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Reset and clear existing data before generation",
        )

    def handle(self, *args, **options):
        """Execute the data generation process."""
        quick = options.get("quick", False)
        full = options.get("full", False) or not quick
        reset = options.get("reset", False)

        self.stdout.write(self.style.SUCCESS("🚀 Starting test data generation..."))

        if reset:
            self.stdout.write(self.style.WARNING("⚠️  Reset option not implemented yet"))

        try:
            # Generate core data
            self.stdout.write("📝 Generating core data...")
            call_command("generate_core_data", model="User", count=10 if quick else 25)
            call_command("generate_customers", count=15 if quick else 50)

            # Generate product data
            self.stdout.write("🛍️  Generating product data...")
            call_command("generate_categories", count=5 if quick else 12)
            call_command("generate_collections", count=3 if quick else 8)
            call_command("generate_products", count=20 if quick else 100)
            call_command("generate_variants", count=30 if quick else 200)
            call_command("generate_reviews", count=50 if quick else 300)

            # Generate order data (if available)
            self.stdout.write("📦 Checking for order data generation...")
            try:
                call_command("generate_orders", count=10 if quick else 50)
            except Exception:
                self.stdout.write(
                    self.style.WARNING(
                        "Order generation command not found, skipping..."
                    )
                )

            # Success message
            mode = "quick" if quick else "full"
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ {mode.title()} test data generation completed successfully!"
                )
            )

            # Show summary
            self._show_summary()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error generating test data: {e}"))
            raise

    def _show_summary(self):
        """Show a summary of generated data."""
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("📊 Test Data Summary"))
        self.stdout.write("=" * 50)

        try:
            from django.contrib.auth import get_user_model

            from core.models import Customer
            from products.models import Category, Collection, Product, ProductVariant

            User = get_user_model()

            counts = {
                "Users": User.objects.count(),
                "Customers": Customer.objects.count(),
                "Categories": Category.objects.count(),
                "Collections": Collection.objects.count(),
                "Products": Product.objects.count(),
                "Product Variants": ProductVariant.objects.count(),
            }

            for model, count in counts.items():
                self.stdout.write(f"• {model}: {count}")

        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not generate summary: {e}"))

        self.stdout.write("\n🎯 You can now:")
        self.stdout.write(
            "• Visit http://localhost:8000/api/docs for API documentation"
        )
        self.stdout.write("• Visit http://localhost:8000/admin for Django admin")
        self.stdout.write(
            "• Use credentials from generated users (password: Test1234!)"
        )
        self.stdout.write("=" * 50 + "\n")
