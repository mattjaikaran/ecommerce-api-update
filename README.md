# Ecommerce API 

2025 update for ecommerce api using Django Ninja/Django Ninja Extra and Postgres


## Technologies
- Python 3.11
- [Django 5.1](https://docs.djangoproject.com/en/5.1/)
- [Django Ninja](https://django-ninja.dev/)
- [Django Ninja Extra](https://eadwincode.github.io/django-ninja-extra/) a collection of extra features for Django Ninja 
- [Django Ninja JWT](https://eadwincode.github.io/django-ninja-jwt/)
    - [Django Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) abstraction for Django Ninja
- [Postgres](https://www.postgresql.org/docs/) database
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Django Unfold Admin](https://unfoldadmin.com/)
    - [Unfold Docs](https://github.com/unfoldadmin/django-unfold)
- Docker & Docker Compose
- pytest for testing
- Gunicorn for production serving

#### Dev Tools & Features
- Makefile to run commands
- PyTest for unit tests
- Custom Start App command to create a new app
    - with extended functionality for Django Ninja, Django Ninja Extra, and Django Unfold
    - `make startapp <app_name>`
- [Faker](https://faker.readthedocs.io/en/master/) for generating fake data.
    - See `@/core/management/commands/generate_core_data.py` for more information
- [Swagger](https://swagger.io/) for API documentation
  - [Localhost Docs](http://localhost:8000/api/docs)
- [Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest) for debugging
- [Django Environ](https://django-environ.readthedocs.io/en/latest/) for managing environment variables
- Linting
    - [Black](https://github.com/psf/black) Formatter
        - Configuration located in `@/.vscode/settings.json`
    - [isort](https://pycqa.github.io/isort/) sorting imports
    - [Flake8](https://flake8.pycqa.org/en/latest/)
    - Will run all 3 with the lint script located in `@/scripts/lint.sh`
        - To run `./scripts/lint.sh`


## Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/mattjaikaran/django-ninja-boilerplate
cd django-ninja-boilerplate

# Create environment file
cp .env.example .env
# Edit .env with your settings

# Start the services
docker-compose up --build
```

Visit http://localhost:8000/api/docs for the API documentation.

## Local Development Setup

```bash
git clone https://github.com/mattjaikaran/django-ninja-boilerplate
cd django-ninja-boilerplate
# Create and activate virtual environment
python3 -m venv env # create a virtual environment using the venv virtual environment
source env/bin/activate # activate the virtual environment
touch .env # create a new env file
# update the .env file with necessary values -> db info, superuser info
pip3 install -r requirements.txt # install dependencies from requirements.txt
python3 manage.py migrate # apply migration files to your local db
python3 manage.py create_superuser # runs custom script to create a superuser
./scripts/generate_secret_key.sh # generate new secret key 
python3 manage.py runserver # run the local server on http://localhost:8000/admin
```

## Commands

### Start a new Django App
```bash
# start a new django app with extended functionality 
# for Django Ninja, Django Ninja Extra, and Django Unfold. 
$ make startapp <app_name> 
```

### Run Server
```bash
$ make runserver
```

### Install a library
This runs pip install <library-name> , then pip freeze > requirements.txt to update the requirements.txt file
```bash
$ make install <library-name>
# example
# make install django-ninja-jwt
```

### Drop DB, Create DB, Migrate, Create Superuser via db-setup script
```bash
$ make db-setup
```

## Developer Experience Scripts

The project includes several powerful scripts to enhance the development workflow, located in the `scripts/` directory.

### Core Scripts Overview

- `test_feature.sh`: Test specific features or endpoints
- `reset_test_data.sh`: Reset and seed test data
- `check_health.sh`: Check API health and dependencies
- `db_setup.sh`: Set up database and run migrations
- `setup.sh`: Initial project setup
- `lint.sh`: Run linting checks
- `generate_secret_key.sh`: Generate Django secret key

### Testing Features

Test specific parts of the API with detailed output:

```bash
# Test all product-related endpoints
./scripts/test_feature.sh products

# Test cart features with verbose output
./scripts/test_feature.sh -v cart

# Test authentication endpoints
./scripts/test_feature.sh auth

# Test all features
./scripts/test_feature.sh all
```

### Managing Test Data

Reset and seed test data for development:

```bash
# Reset all test data
./scripts/reset_test_data.sh

# Reset only product data
./scripts/reset_test_data.sh -a products

# Force reset without confirmation
./scripts/reset_test_data.sh -f

# Reset data without running migrations
./scripts/reset_test_data.sh --no-migrations
```

### Health Checks

Monitor the health of your API and dependencies:

```bash
# Run all health checks
./scripts/check_health.sh

# Run with verbose output
./scripts/check_health.sh -v

# Check specific API URL
./scripts/check_health.sh -u http://localhost:8001

# Skip specific checks
./scripts/check_health.sh --skip-deps --skip-db
```

### Script Features

All developer scripts include:
- Colored output for better visibility
- Verbose mode for detailed information
- Help documentation (`-h` or `--help`)
- Error handling with descriptive messages
- Consistent formatting and logging

For more detailed documentation about the scripts, see `scripts/README.md`.

## Why Django Ninja?
- [Django Ninja Docs](https://django-ninja.dev/)

Django Ninja is a newer framework that can run on Django 5.0, built in OpenAPI/Swagger/ReDoc, has async support, and uses Pydantic. It almost has a FastAPI vibe with some Django features. It seems like there is decent support and an excitement to have a *new* Django Framework.

By following this approach, the front-end can easily consume the JSON data from these endpoints. The API will be self-documenting and you can view the OpenAPI (Swagger) documentation by navigating to `/api/docs` in your browser.

### Why Django Ninja Extra?
- [Django Ninja Extra Docs](https://eadwincode.github.io/django-ninja-extra/)

When building Django apps, I am mostly familiar with a class-based views architecture and ninja-extra makes the transition from DRF to ninja a little easier. There are permissions and dependency injection included. 

### Django Ninja Serialization

- Django Ninja uses Pydantic models (Schemas) for serialization, not Django serializers like in DRF.
- The response parameter in the route decorator specifies the expected response format.
- Use from_orm() to convert Django ORM objects to Pydantic models.
- Django Ninja automatically handles the conversion to JSON in the HTTP response.

## Admin Panel
- [Django Unfold Docs](https://github.com/unfoldadmin/django-unfold)

Django Unfold has one of the cleaniest designs for Django admin panels. Pretty easy to get set up and there is now support for certain libraries that broke the design (ie - django-import-export)

## Production Deployment

1. Update `.env` with production settings
2. Build and run with Docker:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest path/to/test_file.py

# Run with coverage
pytest --cov=.
```

## API Documentation
- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`

## Features
- JWT Authentication
- PostgreSQL Database
- Docker & Docker Compose setup
- Comprehensive test setup with pytest
- Code formatting with Black and isort
- Production-ready with Gunicorn
- Environment-based settings
- Custom user model
- Admin panel with Django Unfold
- API throttling and pagination
- CORS configuration
- Debug toolbar for development

## Database

```bash
$ psql my_db # enter shell
$ createdb --username=USERNAME my_db # create db
$ dropdb my_db # drop db
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
