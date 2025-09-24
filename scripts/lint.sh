#!/bin/bash

# lint.sh - Modern linting and formatting with ruff

echo "🔍 Running ruff linting..."
uv run ruff check .

echo "✨ Running ruff formatting..."
uv run ruff format .

echo "✅ Linting and formatting complete!"