from django.apps import apps
from django.core.cache import cache
from django.db.models import Q, Count
from typing import Dict, Any, List
from .warming import CacheWarmer
from .versioning import VersionedCache
import logging

logger = logging.getLogger(__name__)


class CachePreloader:
    """
    Manages preloading of common queries and data patterns.
    Usage:
        preloader = CachePreloader()
        preloader.preload_all()
        # Or specific preloads:
        preloader.preload_products()
    """

    def __init__(self):
        self.warmer = CacheWarmer()

    def preload_all(self):
        """Preload all common queries."""
        logger.info("Starting cache preload for all common queries")

        # Call all preload methods
        for method_name in dir(self):
            if method_name.startswith("preload_") and method_name != "preload_all":
                method = getattr(self, method_name)
                if callable(method):
                    try:
                        method()
                    except Exception as e:
                        logger.error(f"Error in {method_name}: {e}")

        logger.info("Completed cache preload for all common queries")

    def preload_products(self):
        """Preload common product queries."""
        try:
            Product = apps.get_model("products", "Product")

            # Common product querysets
            querysets = [
                ("featured_products", Product.objects.filter(featured=True)),
                ("popular_products", Product.objects.filter(popular=True)),
                ("new_arrivals", Product.objects.order_by("-created_at")[:12]),
                ("on_sale", Product.objects.filter(on_sale=True)),
            ]

            # Warm these querysets
            self.warmer.warm_querysets(querysets)

            # Warm individual popular products
            popular_products = Product.objects.filter(
                Q(popular=True) | Q(featured=True)
            )
            self.warmer.warm_model(
                Product, queryset=popular_products, timeout=3600  # 1 hour
            )

            logger.info("Completed product cache preload")

        except Exception as e:
            logger.error(f"Error preloading products: {e}")

    def preload_categories(self):
        """Preload category hierarchy and stats."""
        try:
            Category = apps.get_model("products", "Category")
            Product = apps.get_model("products", "Product")

            # Get categories with product counts
            categories = Category.objects.annotate(product_count=Count("products"))

            # Build category tree with stats
            category_tree = self._build_category_tree(categories)

            # Cache the tree
            versioned_cache = VersionedCache("categories")
            versioned_cache.set("category_tree", category_tree, timeout=3600)

            logger.info("Completed category cache preload")

        except Exception as e:
            logger.error(f"Error preloading categories: {e}")

    def preload_cart_data(self):
        """Preload common cart-related queries."""
        try:
            Cart = apps.get_model("cart", "Cart")

            # Preload active cart items with product data
            active_carts = (
                Cart.objects.filter(status="active")
                .select_related("user")
                .prefetch_related("items__product")
            )

            self.warmer.warm_querysets([("active_carts", active_carts)])

            logger.info("Completed cart cache preload")

        except Exception as e:
            logger.error(f"Error preloading cart data: {e}")

    def preload_user_data(self):
        """Preload common user-related queries."""
        try:
            User = apps.get_model("core", "User")

            # Preload active users with profiles
            active_users = User.objects.filter(is_active=True).select_related("profile")

            self.warmer.warm_querysets([("active_users", active_users)])

            logger.info("Completed user cache preload")

        except Exception as e:
            logger.error(f"Error preloading user data: {e}")

    def _build_category_tree(self, categories) -> List[Dict[str, Any]]:
        """Build a hierarchical category tree with stats."""

        def build_node(category):
            return {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "product_count": category.product_count,
                "children": [
                    build_node(child)
                    for child in categories
                    if child.parent_id == category.id
                ],
            }

        # Build tree starting from root categories
        return [
            build_node(category)
            for category in categories
            if category.parent_id is None
        ]
