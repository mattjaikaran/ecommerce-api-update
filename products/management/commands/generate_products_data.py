# products/management/commands/generate_products_data.py
from django.core.management.base import BaseCommand
from products.models import Products
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Generate sample data for Products'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of products to create')

    def handle(self, *args, **options):
        count = options['count']
        for i in range(count):
            Products.objects.create(
                name=f'Products {get_random_string(5)}',
                description=f'Description for products {i+1}'
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} products'))
