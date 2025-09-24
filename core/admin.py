import json

from django.apps import apps
from django.contrib import admin, messages
from django.core.cache import cache
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from unfold.admin import ModelAdmin

from .admin import CustomerFeedbackAdmin, UserAdmin
from .cache.versioning import VersionedCache
from .cache.warming import CacheWarmer

__all__ = [
    UserAdmin,
    CustomerFeedbackAdmin,
]


class CacheMonitorAdmin(admin.AdminSite, ModelAdmin):
    """Custom admin site with cache monitoring."""

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "cache-monitor/",
                self.admin_view(self.cache_monitor_view),
                name="cache-monitor",
            ),
            path(
                "cache-monitor/clear/<str:namespace>/",
                self.admin_view(self.clear_cache_view),
                name="clear-cache",
            ),
            path(
                "cache-monitor/warm/<str:model_name>/",
                self.admin_view(self.warm_cache_view),
                name="warm-cache",
            ),
        ]
        return custom_urls + urls

    def cache_monitor_view(self, request):
        """View for monitoring cache status."""
        # Get cache statistics
        stats = cache.info()

        # Get all models for cache warming
        models = []
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                if not model._meta.abstract:
                    namespace = model._meta.model_name
                    versioned_cache = VersionedCache(namespace)
                    version = versioned_cache.get()
                    models.append(
                        {
                            "name": model._meta.verbose_name.title(),
                            "namespace": namespace,
                            "version": version,
                            "count": model.objects.count(),
                        }
                    )

        # Format cache info for display
        if isinstance(stats, dict):
            formatted_stats = json.dumps(stats, indent=2)
        else:
            formatted_stats = str(stats)

        context = {
            "title": "Cache Monitor",
            "stats": formatted_stats,
            "models": models,
            "is_nav_sidebar_enabled": True,
            "available_apps": self.get_app_list(request),
        }

        return TemplateResponse(request, "admin/cache_monitor.html", context)

    def clear_cache_view(self, request, namespace):
        """View for clearing cache for a specific namespace."""
        versioned_cache = VersionedCache(namespace)
        versioned_cache.invalidate_all()
        messages.success(request, f"Cache cleared for {namespace}")
        return redirect("admin:cache-monitor")

    def warm_cache_view(self, request, model_name):
        """View for warming cache for a specific model."""
        # Find model by name
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                if model._meta.model_name == model_name:
                    warmer = CacheWarmer()
                    warmer.warm_model(model)
                    messages.success(
                        request, f"Cache warmed for {model._meta.verbose_name_plural}"
                    )
                    return redirect("admin:cache-monitor")

        messages.error(request, f"Model {model_name} not found")
        return redirect("admin:cache-monitor")
