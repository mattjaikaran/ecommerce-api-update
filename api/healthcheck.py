"""Health check module for the ecommerce API.

This module provides health check endpoints and utilities to monitor
the status of various services and dependencies.
"""

import time
from datetime import UTC, datetime
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse

from .constants import HEALTH_CHECK_SERVICES


class HealthChecker:
    """Health check utility class."""

    def __init__(self):
        self.checks = {
            "database": self._check_database,
            "redis": self._check_redis,
            "s3": self._check_s3,
            "stripe": self._check_stripe,
        }

    def check_all(self) -> dict[str, Any]:
        """Run all health checks."""
        results = {
            "status": "healthy",
            "timestamp": datetime.now(UTC).isoformat(),
            "services": {},
            "summary": {
                "total": len(HEALTH_CHECK_SERVICES),
                "healthy": 0,
                "unhealthy": 0,
            },
        }

        overall_healthy = True

        for service in HEALTH_CHECK_SERVICES:
            if service in self.checks:
                start_time = time.time()
                check_result = self.checks[service]()
                end_time = time.time()

                results["services"][service] = {
                    **check_result,
                    "response_time_ms": round((end_time - start_time) * 1000, 2),
                }

                if check_result["status"] == "healthy":
                    results["summary"]["healthy"] += 1
                else:
                    results["summary"]["unhealthy"] += 1
                    overall_healthy = False
            else:
                results["services"][service] = {
                    "status": "unknown",
                    "message": "No health check implemented",
                }
                results["summary"]["unhealthy"] += 1
                overall_healthy = False

        results["status"] = "healthy" if overall_healthy else "unhealthy"
        return results

    def check_service(self, service_name: str) -> dict[str, Any]:
        """Check a specific service."""
        if service_name not in self.checks:
            return {
                "status": "unknown",
                "message": f"No health check for service: {service_name}",
            }

        start_time = time.time()
        result = self.checks[service_name]()
        end_time = time.time()

        result["response_time_ms"] = round((end_time - start_time) * 1000, 2)
        return result

    def _check_database(self) -> dict[str, Any]:
        """Check database connectivity."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

            return {"status": "healthy", "message": "Database connection successful"}
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Database connection failed: {e!s}",
            }

    def _check_redis(self) -> dict[str, Any]:
        """Check Redis connectivity."""
        try:
            # Test cache connection
            test_key = "healthcheck:redis:test"
            test_value = "test_value"

            cache.set(test_key, test_value, 60)
            retrieved_value = cache.get(test_key)

            if retrieved_value == test_value:
                cache.delete(test_key)
                return {"status": "healthy", "message": "Redis connection successful"}
            return {
                "status": "unhealthy",
                "message": "Redis data integrity check failed",
            }
        except Exception as e:
            return {"status": "unhealthy", "message": f"Redis connection failed: {e!s}"}

    def _check_s3(self) -> dict[str, Any]:
        """Check S3 connectivity."""
        try:
            if not getattr(settings, "USE_S3", False):
                return {"status": "skipped", "message": "S3 not configured"}

            from django.core.files.storage import default_storage

            # Try to list files in the bucket
            default_storage.listdir("")

            return {"status": "healthy", "message": "S3 connection successful"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"S3 connection failed: {e!s}"}

    def _check_stripe(self) -> dict[str, Any]:
        """Check Stripe connectivity."""
        try:
            stripe_key = getattr(settings, "STRIPE_SECRET_KEY", None)
            if not stripe_key:
                return {"status": "skipped", "message": "Stripe not configured"}

            import stripe

            stripe.api_key = stripe_key

            # Make a simple API call to check connectivity
            stripe.Account.retrieve()

            return {"status": "healthy", "message": "Stripe connection successful"}
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Stripe connection failed: {e!s}",
            }


# Health check views


def health_check_all(request):
    """Endpoint for checking all services."""
    checker = HealthChecker()
    results = checker.check_all()

    status_code = 200 if results["status"] == "healthy" else 503
    return JsonResponse(results, status=status_code)


def health_check_simple(request):
    """Simple health check endpoint."""
    return JsonResponse(
        {
            "status": "healthy",
            "message": "API is running",
            "timestamp": datetime.now(UTC).isoformat(),
        }
    )


def health_check_service(request, service_name):
    """Endpoint for checking a specific service."""
    checker = HealthChecker()
    result = checker.check_service(service_name)

    status_code = 200 if result["status"] == "healthy" else 503
    return JsonResponse({"service": service_name, **result}, status=status_code)


def readiness_check(request):
    """Readiness check for Kubernetes/container orchestration."""
    checker = HealthChecker()

    # Check critical services only
    critical_services = ["database"]
    all_ready = True

    for service in critical_services:
        result = checker.check_service(service)
        if result["status"] != "healthy":
            all_ready = False
            break

    if all_ready:
        return JsonResponse(
            {"status": "ready", "message": "Service is ready to receive traffic"}
        )
    return JsonResponse(
        {"status": "not_ready", "message": "Service is not ready to receive traffic"},
        status=503,
    )


def liveness_check(request):
    """Liveness check for Kubernetes/container orchestration."""
    # Simple check to see if the application is still running
    return JsonResponse(
        {
            "status": "alive",
            "message": "Service is alive",
            "timestamp": datetime.now(UTC).isoformat(),
        }
    )


# Utility functions


def get_system_info() -> dict[str, Any]:
    """Get system information."""
    import platform
    import sys

    import django

    return {
        "python_version": sys.version,
        "django_version": django.get_version(),
        "platform": platform.platform(),
        "architecture": platform.architecture(),
        "hostname": platform.node(),
    }


def get_database_info() -> dict[str, Any]:
    """Get database information."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]

        return {
            "engine": connection.vendor,
            "version": version,
            "database": connection.settings_dict["NAME"],
        }
    except Exception as e:
        return {"error": str(e)}


def monitoring_info(request):
    """Comprehensive monitoring information."""
    checker = HealthChecker()

    return JsonResponse(
        {
            "health": checker.check_all(),
            "system": get_system_info(),
            "database": get_database_info(),
            "settings": {
                "debug": settings.DEBUG,
                "allowed_hosts": settings.ALLOWED_HOSTS,
                "time_zone": settings.TIME_ZONE,
            },
        }
    )
