import logging

from django.apps import apps
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .versioning import VersionedCache

logger = logging.getLogger(__name__)


def register_cache_signals():
    """Register cache invalidation signals for all models."""
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if not model._meta.abstract:
                # Register save signal
                post_save.connect(
                    invalidate_model_cache,
                    sender=model,
                    dispatch_uid=f"cache_invalidate_save_{model._meta.model_name}",
                )
                # Register delete signal
                post_delete.connect(
                    invalidate_model_cache,
                    sender=model,
                    dispatch_uid=f"cache_invalidate_delete_{model._meta.model_name}",
                )
                logger.info(f"Registered cache signals for {model._meta.model_name}")


@receiver([post_save, post_delete])
def invalidate_model_cache(sender, instance, **kwargs):
    """Invalidate cache when a model instance is saved or deleted."""
    try:
        # Get the model namespace
        namespace = sender._meta.model_name

        # Create versioned cache instance
        versioned_cache = VersionedCache(namespace)

        # Invalidate all cache for this model
        versioned_cache.invalidate_all()

        # Log the invalidation
        logger.info(f"Invalidated cache for {namespace} - Instance ID: {instance.pk}")

        # Handle related models if needed
        handle_related_models(sender, instance)

    except Exception as e:
        logger.error(f"Error invalidating cache for {sender._meta.model_name}: {e}")


def handle_related_models(model, instance):
    """Invalidate cache for related models."""
    try:
        # Get all related fields
        for field in model._meta.get_fields():
            # Handle forward relationships
            if hasattr(field, "related_model") and field.related_model:
                related_namespace = field.related_model._meta.model_name
                versioned_cache = VersionedCache(related_namespace)
                versioned_cache.invalidate_all()
                logger.info(f"Invalidated related cache for {related_namespace}")

            # Handle reverse relationships
            if hasattr(field, "remote_field") and field.remote_field:
                if hasattr(field.remote_field, "model"):
                    remote_namespace = field.remote_field.model._meta.model_name
                    versioned_cache = VersionedCache(remote_namespace)
                    versioned_cache.invalidate_all()
                    logger.info(
                        f"Invalidated reverse related cache for {remote_namespace}"
                    )

    except Exception as e:
        logger.error(f"Error handling related models for {model._meta.model_name}: {e}")
