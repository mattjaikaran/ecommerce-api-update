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

# other scripts here
echo "Generating sample data..."
python manage.py generate_categories --count=10 --parent_count=5
python manage.py generate_products --count=50
python manage.py generate_variants --min_variants=2 --max_variants=5
python manage.py generate_reviews 100 --verified-ratio 0.7 --featured-ratio 0.2
python manage.py generate_carts 20 --min-items 1 --max-items 5 --abandoned-ratio 0.3
python manage.py generate_orders 30 --min-items 1 --max-items 5
python manage.py generate_fulfillments --status-ratio 0.7
echo "Sample data generated"

echo ">>> db_setup complete"

echo ">>> Running development server..."
python3 manage.py runserver

