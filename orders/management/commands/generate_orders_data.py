# orders/management/commands/generate_orders_data.py
from django.core.management.base import BaseCommand
from orders.models import Orders
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Generate sample data for Orders'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of orders to create')

    def handle(self, *args, **options):
        count = options['count']
        for i in range(count):
            Orders.objects.create(
                name=f'Orders {get_random_string(5)}',
                description=f'Description for orders {i+1}'
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} orders'))
