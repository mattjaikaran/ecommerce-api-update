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

# Copy dependency files and README for build
COPY pyproject.toml uv.lock README.md ./

# Install Python dependencies from pyproject.toml
RUN uv pip install --system --no-cache -e .

# Create logs directory
RUN mkdir -p /app/logs

# Copy project
COPY . .

# Copy and set permissions for entrypoint scripts
COPY docker-entrypoint.sh docker-entrypoint-dev.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint-dev.sh

# Create a non-root user and fix permissions
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Collect static files (will be overridden in docker-compose for dev)
RUN python manage.py collectstatic --noinput --settings=api.settings.prod || true

# Default command (will be overridden in docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "api.wsgi:application"]