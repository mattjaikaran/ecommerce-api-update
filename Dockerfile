FROM python:3.12-slim

# Set environment variables optimized for OrbStack
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
# OrbStack optimizations
ENV DOCKER_BUILDKIT=1
ENV BUILDKIT_PROGRESS=plain

# Set work directory
WORKDIR /app

# Install system dependencies and uv
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        gcc \
        curl \
        build-essential \
        netcat-openbsd \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create virtual environment and install Python dependencies using uv
RUN uv venv .venv && \
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

# Create logs directory
RUN mkdir -p /app/logs

# Copy project
COPY . .

# Copy and set permissions for entrypoint scripts
COPY docker-entrypoint.sh docker-entrypoint-dev.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint-dev.sh

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Collect static files (will be overridden in docker-compose for dev)
RUN .venv/bin/python manage.py collectstatic --noinput --settings=api.settings.prod || true

# Update PATH to include virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Default command (will be overridden in docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "api.wsgi:application"]