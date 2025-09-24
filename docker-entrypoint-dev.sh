#!/bin/bash

# Development entrypoint script

set -e

echo "Development mode: Installing dependencies..."

# Install dependencies using uv if virtual environment doesn't exist or Django is not installed
if [ ! -d ".venv" ] || ! .venv/bin/python -c "import django" 2>/dev/null; then
    echo "Creating virtual environment and installing dependencies..."
    uv venv .venv
    uv pip install --python .venv/bin/python --no-cache \
        "Django>=5.1.4,<5.2" \
        "django-environ>=0.11.2" \
        "psycopg2-binary>=2.9.10" \
        "django-cors-headers>=4.6.0" \
        "django-debug-toolbar>=4.4.6" \
        "django-flags>=5.0.13" \
        "django-import-export>=4.3.1" \
        "django-js-asset>=2.2.0" \
        "django-mptt>=0.16.0" \
        "django-redis>=5.4.0" \
        "django-storages>=1.14.4" \
        "django-unfold>=0.43.0" \
        "django-ninja>=1.3.0" \
        "django-ninja-extra>=0.21.8" \
        "django-ninja-jwt>=5.3.4" \
        "redis>=5.2.1" \
        "hiredis>=3.1.0" \
        "celery>=5.3.0" \
        "django-celery-beat>=2.5.0" \
        "django-celery-results>=2.5.0" \
        "flower>=2.0.1" \
        "gunicorn>=21.0.0"
else
    echo "Virtual environment already exists"
fi

# Add virtual environment to PATH
export PATH="/app/.venv/bin:$PATH"

# Wait for database and redis if they're needed
if [ "$1" = "python" ] && [[ "$2" == *"manage.py"* ]]; then
    echo "Waiting for database and redis..."
    if [ "$DB_HOST" ] && [ "$DB_PORT" ]; then
        while ! nc -z "$DB_HOST" "$DB_PORT"; do
            sleep 1
        done
        echo "Database is ready!"
    fi
    
    if [ "$REDIS_URL" ]; then
        REDIS_HOST=$(echo "$REDIS_URL" | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
        REDIS_PORT=$(echo "$REDIS_URL" | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        
        if [ "$REDIS_HOST" ] && [ "$REDIS_PORT" ]; then
            while ! nc -z "$REDIS_HOST" "$REDIS_PORT"; do
                sleep 1
            done
            echo "Redis is ready!"
        fi
    fi
fi

# Execute the command
exec "$@"
