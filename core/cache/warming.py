from django.core.cache import cache
from django.conf import settings
from django.db.models import Model, QuerySet
from typing import List, Type, Optional, Any, Dict
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from .versioning import VersionedCache

logger = logging.getLogger(__name__)


class CacheWarmer:
    """
    Manages cache warming for different data types.
    Usage:
        warmer = CacheWarmer()
        warmer.warm_model(Product, chunk_size=100)
        warmer.warm_querysets([
            ('popular_products', Product.objects.filter(popular=True)),
            ('featured_products', Product.objects.filter(featured=True))
        ])
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def warm_model(
        self, model: Type[Model], chunk_size: int = 100, timeout: Optional[int] = None
    ) -> None:
        """Warm cache for all instances of a model."""
        cache_ns = model._meta.model_name
        versioned_cache = VersionedCache(cache_ns)

        # Get total count for logging
        total = model.objects.count()
        processed = 0
        start_time = time.time()

        logger.info(f"Starting cache warming for {model.__name__}, {total} items")

        # Process in chunks for memory efficiency
        for chunk in self._chunked_queryset(model.objects.all(), chunk_size):
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Create cache tasks
                futures = []
                for instance in chunk:
                    cache_key = f"{model._meta.model_name}:{instance.pk}"
                    futures.append(
                        executor.submit(
                            versioned_cache.set, cache_key, instance, timeout
                        )
                    )

                # Wait for all tasks to complete
                for future in futures:
                    future.result()

            processed += len(chunk)
            logger.info(f"Warmed {processed}/{total} {model.__name__} instances")

        duration = time.time() - start_time
        logger.info(
            f"Completed warming {total} {model.__name__} instances in {duration:.2f}s"
        )

    def warm_querysets(
        self, querysets: List[tuple[str, QuerySet]], timeout: Optional[int] = None
    ) -> None:
        """
        Warm cache for specific querysets.
        Args:
            querysets: List of (cache_key, queryset) tuples
            timeout: Cache timeout in seconds
        """
        start_time = time.time()
        total = len(querysets)

        logger.info(f"Starting cache warming for {total} querysets")

        for idx, (cache_key, queryset) in enumerate(querysets, 1):
            # Get model name for namespace
            model = queryset.model
            cache_ns = model._meta.model_name
            versioned_cache = VersionedCache(cache_ns)

            # Cache the queryset
            versioned_cache.set(cache_key, list(queryset), timeout)

            logger.info(f"Warmed queryset {idx}/{total}: {cache_key}")

        duration = time.time() - start_time
        logger.info(f"Completed warming {total} querysets in {duration:.2f}s")

    def warm_custom_data(
        self,
        namespace: str,
        data_items: List[tuple[str, Any]],
        timeout: Optional[int] = None,
    ) -> None:
        """
        Warm cache with custom data items.
        Args:
            namespace: Cache namespace
            data_items: List of (cache_key, data) tuples
            timeout: Cache timeout in seconds
        """
        versioned_cache = VersionedCache(namespace)
        start_time = time.time()
        total = len(data_items)

        logger.info(f"Starting cache warming for {total} custom items")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for cache_key, data in data_items:
                futures.append(
                    executor.submit(versioned_cache.set, cache_key, data, timeout)
                )

            # Wait for all tasks to complete
            for future in futures:
                future.result()

        duration = time.time() - start_time
        logger.info(f"Completed warming {total} custom items in {duration:.2f}s")

    @staticmethod
    def _chunked_queryset(queryset: QuerySet, chunk_size: int):
        """Split a queryset into chunks for efficient processing."""
        start = 0
        while True:
            chunk = queryset[start : start + chunk_size]
            if not chunk:
                break
            yield chunk
            start += chunk_size
