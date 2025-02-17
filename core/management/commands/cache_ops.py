from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.cache import cache
from core.cache.warming import CacheWarmer
from core.cache.preload import CachePreloader
from core.cache.versioning import VersionedCache
from typing import List, Any
import time
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Manage cache operations (warm, clear, preload, etc.)"

    def add_arguments(self, parser):
        parser.add_argument(
            "operation",
            choices=["warm", "clear", "preload", "stats", "version"],
            help="Operation to perform",
        )
        parser.add_argument(
            "--models",
            nargs="+",
            help="Specific models to operate on (e.g., products.Product)",
        )
        parser.add_argument(
            "--chunk-size",
            type=int,
            default=100,
            help="Chunk size for warming operations",
        )
        parser.add_argument("--timeout", type=int, help="Cache timeout in seconds")
        parser.add_argument(
            "--force", action="store_true", help="Force operation without confirmation"
        )

    def handle(self, *args, **options):
        operation = options["operation"]
        models = options["models"]
        chunk_size = options["chunk_size"]
        timeout = options["timeout"]
        force = options["force"]

        # Confirm dangerous operations
        if operation in ["clear"] and not force:
            if not self.confirm_operation(operation):
                self.stdout.write(self.style.WARNING("Operation cancelled"))
                return

        # Execute requested operation
        start_time = time.time()

        try:
            if operation == "warm":
                self.warm_cache(models, chunk_size, timeout)
            elif operation == "clear":
                self.clear_cache(models)
            elif operation == "preload":
                self.preload_cache(models)
            elif operation == "stats":
                self.show_stats()
            elif operation == "version":
                self.show_versions(models)

            duration = time.time() - start_time
            self.stdout.write(
                self.style.SUCCESS(f"Operation completed in {duration:.2f} seconds")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during operation: {str(e)}"))
            logger.error(f"Cache operation error: {str(e)}", exc_info=True)

    def warm_cache(self, models: List[str], chunk_size: int, timeout: int) -> None:
        """Warm cache for specified models."""
        warmer = CacheWarmer()

        if models:
            # Warm specific models
            for model_path in models:
                try:
                    app_label, model_name = model_path.split(".")
                    model = apps.get_model(app_label, model_name)
                    self.stdout.write(f"Warming cache for {model_path}...")
                    warmer.warm_model(model, chunk_size, timeout)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error warming {model_path}: {str(e)}")
                    )
        else:
            # Warm all models
            for app_config in apps.get_app_configs():
                for model in app_config.get_models():
                    if not model._meta.abstract:
                        self.stdout.write(f"Warming cache for {model._meta.label}...")
                        warmer.warm_model(model, chunk_size, timeout)

    def clear_cache(self, models: List[str]) -> None:
        """Clear cache for specified models."""
        if models:
            # Clear specific models
            for model_path in models:
                try:
                    app_label, model_name = model_path.split(".")
                    model = apps.get_model(app_label, model_name)
                    namespace = model._meta.model_name
                    versioned_cache = VersionedCache(namespace)
                    versioned_cache.invalidate_all()
                    self.stdout.write(
                        self.style.SUCCESS(f"Cleared cache for {model_path}")
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error clearing {model_path}: {str(e)}")
                    )
        else:
            # Clear all cache
            cache.clear()
            self.stdout.write(self.style.SUCCESS("Cleared all cache"))

    def preload_cache(self, models: List[str]) -> None:
        """Preload cache with common queries."""
        preloader = CachePreloader()

        if models:
            # Preload specific models
            for model_path in models:
                try:
                    method_name = f'preload_{model_path.split(".")[-1].lower()}s'
                    if hasattr(preloader, method_name):
                        self.stdout.write(f"Preloading {model_path}...")
                        getattr(preloader, method_name)()
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"No preload method for {model_path}")
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error preloading {model_path}: {str(e)}")
                    )
        else:
            # Preload all
            self.stdout.write("Preloading all common queries...")
            preloader.preload_all()

    def show_stats(self) -> None:
        """Show cache statistics."""
        stats = cache.info()
        self.stdout.write("\nCache Statistics:")
        self.stdout.write("-" * 40)

        if isinstance(stats, dict):
            for key, value in stats.items():
                self.stdout.write(f"{key}: {value}")
        else:
            self.stdout.write(str(stats))

    def show_versions(self, models: List[str]) -> None:
        """Show cache versions for models."""
        self.stdout.write("\nCache Versions:")
        self.stdout.write("-" * 40)

        if models:
            # Show versions for specific models
            for model_path in models:
                try:
                    app_label, model_name = model_path.split(".")
                    model = apps.get_model(app_label, model_name)
                    namespace = model._meta.model_name
                    versioned_cache = VersionedCache(namespace)
                    version = versioned_cache.get()
                    self.stdout.write(f"{model_path}: {version}")
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error getting version for {model_path}: {str(e)}"
                        )
                    )
        else:
            # Show versions for all models
            for app_config in apps.get_app_configs():
                for model in app_config.get_models():
                    if not model._meta.abstract:
                        namespace = model._meta.model_name
                        versioned_cache = VersionedCache(namespace)
                        version = versioned_cache.get()
                        self.stdout.write(f"{model._meta.label}: {version}")

    def confirm_operation(self, operation: str) -> bool:
        """Confirm dangerous operations."""
        self.stdout.write(
            self.style.WARNING(
                f"You are about to {operation} the cache. "
                "This operation cannot be undone."
            )
        )
        return input("Are you sure you want to continue? [y/N] ").lower() == "y"
