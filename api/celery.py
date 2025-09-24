"""Celery configuration for the api project.

This module sets up Celery for handling asynchronous tasks and periodic tasks.
"""

import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings.dev")

app = Celery("api")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure Celery Beat
app.conf.beat_schedule = {
    # Example periodic task - you can add your own here
    "cleanup-expired-sessions": {
        "task": "core.tasks.cleanup_expired_sessions",
        "schedule": 3600.0,  # Run every hour
    },
}

app.conf.timezone = "UTC"


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f"Request: {self.request!r}")
