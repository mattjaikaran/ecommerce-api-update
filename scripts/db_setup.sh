# !/bin/bash
echo ">>> db_setup initialization"

# Source the .env file
source .env
echo "Database User: $DB_USER"
echo "Database Name: $DB_NAME"
echo "Database Password: $DB_PASSWORD"


echo ">>> db setup - running db_setup.sh"
echo "dropping db $DB_NAME"
dropdb $DB_NAME
echo "$DB_NAME db dropped"

echo "creating new db..."
createdb --username=$DB_USER $DB_NAME
echo "db created"

echo "Updating Pip"
pip install --upgrade pip

echo "Creating static files..."
python manage.py collectstatic --no-input
echo "static files generated"

echo "migrating..."
python3 manage.py migrate --no-input
echo "migrate successful"

echo "creating superuser..."
python3 manage.py create_superuser # creates superuser based on env file data
echo "created superuser"

# Generate Core Data
echo "Generating core data..."
python manage.py generate_core_data --model=User --count=50
python manage.py generate_customers 30 --address-ratio=0.8
echo "Core data generated"

# Generate Product Data
echo "Generating product data..."
python manage.py generate_categories 10 --parent-count=5
python manage.py generate_products 50
python manage.py generate_variants --min-variants=2 --max-variants=5
python manage.py generate_collections 5 --min-products=5 --max-products=20
python manage.py generate_reviews 100 --verified-ratio=0.7 --featured-ratio=0.2
python manage.py generate_product_data --options-count=5 --attributes-count=10 --bundles-count=5 --tags-count=15
echo "Product data generated"

# Generate Cart Data
echo "Generating cart data..."
python manage.py generate_carts 20 --min-items=1 --max-items=5 --abandoned-ratio=0.3
echo "Cart data generated"

# Generate Order Data
echo "Generating order data..."
python manage.py generate_orders 30 --min-items=1 --max-items=5
python manage.py generate_fulfillments --status-ratio=0.7
echo "Order data generated"

echo "Sample data generated"

echo ">>> db_setup complete"

echo ">>> Running development server..."
python3 manage.py runserver

