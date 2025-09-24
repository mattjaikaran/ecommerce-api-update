# Makefile for Django Ecommerce API

.PHONY: help build up down logs shell migrate createsuperuser test lint format clean

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_PROD = docker-compose -f docker-compose.prod.yml
DJANGO_SERVICE = django
DB_SERVICE = db
REDIS_SERVICE = redis
CELERY_SERVICE = celery

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development commands
build: ## Build the Docker images
	$(DOCKER_COMPOSE) build

up: ## Start the development environment
	$(DOCKER_COMPOSE) up -d

up-build: ## Build and start the development environment
	$(DOCKER_COMPOSE) up -d --build

down: ## Stop the development environment
	$(DOCKER_COMPOSE) down

down-volumes: ## Stop the development environment and remove volumes
	$(DOCKER_COMPOSE) down -v

logs: ## Show logs for all services
	$(DOCKER_COMPOSE) logs -f

logs-django: ## Show logs for the django service
	$(DOCKER_COMPOSE) logs -f $(DJANGO_SERVICE)

logs-celery: ## Show logs for the celery service
	$(DOCKER_COMPOSE) logs -f $(CELERY_SERVICE)

logs-db: ## Show logs for the database service
	$(DOCKER_COMPOSE) logs -f $(DB_SERVICE)

logs-redis: ## Show logs for the redis service
	$(DOCKER_COMPOSE) logs -f $(REDIS_SERVICE)

# Django management commands
shell: ## Open Django shell
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) python manage.py shell

shell-plus: ## Open Django shell with shell_plus (if available)
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) python manage.py shell_plus

migrate: ## Run Django migrations
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) python manage.py migrate

makemigrations: ## Create Django migrations
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) python manage.py makemigrations

createsuperuser: ## Create Django superuser
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) python manage.py createsuperuser

collectstatic: ## Collect static files
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) python manage.py collectstatic --noinput

# Database commands
db-shell: ## Open database shell
	$(DOCKER_COMPOSE) exec $(DB_SERVICE) psql -U postgres -d ecommerce_db

db-backup: ## Backup database
	$(DOCKER_COMPOSE) exec $(DB_SERVICE) pg_dump -U postgres ecommerce_db > backup_$$(date +%Y%m%d_%H%M%S).sql

db-restore: ## Restore database (usage: make db-restore FILE=backup.sql)
	$(DOCKER_COMPOSE) exec -T $(DB_SERVICE) psql -U postgres -d ecommerce_db < $(FILE)

# Redis commands
redis-cli: ## Open Redis CLI
	$(DOCKER_COMPOSE) exec $(REDIS_SERVICE) redis-cli

redis-flush: ## Flush Redis cache
	$(DOCKER_COMPOSE) exec $(REDIS_SERVICE) redis-cli FLUSHALL

# Celery commands
celery-shell: ## Open Celery shell
	$(DOCKER_COMPOSE) exec $(CELERY_SERVICE) celery -A api shell

celery-purge: ## Purge all Celery tasks
	$(DOCKER_COMPOSE) exec $(CELERY_SERVICE) celery -A api purge -f

celery-status: ## Show Celery worker status
	$(DOCKER_COMPOSE) exec $(CELERY_SERVICE) celery -A api status

celery-inspect: ## Inspect Celery workers
	$(DOCKER_COMPOSE) exec $(CELERY_SERVICE) celery -A api inspect stats

# Testing and quality
test: ## Run tests
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) python -m pytest

test-coverage: ## Run tests with coverage
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) python -m pytest --cov=. --cov-report=html

lint: ## Run linting
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) ruff check .

format: ## Format code
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) ruff format .

format-check: ## Check code formatting
	$(DOCKER_COMPOSE) exec $(DJANGO_SERVICE) ruff format --check .

# Production commands
prod-build: ## Build production images
	$(DOCKER_COMPOSE_PROD) build

prod-up: ## Start production environment
	$(DOCKER_COMPOSE_PROD) up -d

prod-down: ## Stop production environment
	$(DOCKER_COMPOSE_PROD) down

prod-logs: ## Show production logs
	$(DOCKER_COMPOSE_PROD) logs -f

# Utility commands
clean: ## Clean up Docker resources
	docker system prune -f
	docker volume prune -f

clean-all: ## Clean up all Docker resources (images, volumes, networks)
	docker system prune -a -f
	docker volume prune -f

restart: ## Restart all services
	$(DOCKER_COMPOSE) restart

restart-django: ## Restart django service
	$(DOCKER_COMPOSE) restart $(DJANGO_SERVICE)

restart-celery: ## Restart celery service
	$(DOCKER_COMPOSE) restart $(CELERY_SERVICE)

# Health checks
health: ## Check service health
	@echo "Checking service health..."
	@curl -f http://localhost:8000/health/ || echo "Web service not responding"
	@curl -f http://localhost:5555/ || echo "Flower not responding"

# Setup commands
setup: ## Initial setup for development
	@echo "Setting up development environment..."
	$(MAKE) build
	$(MAKE) up
	@echo "Waiting for services to start..."
	@sleep 10
	$(MAKE) migrate
	@echo "Setup complete! Visit http://localhost:8000"

setup-env: ## Create .env file from example
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo ".env file created from env.example"; \
		echo "Please edit .env file with your configuration"; \
	else \
		echo ".env file already exists"; \
	fi