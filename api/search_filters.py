"""Advanced search and filtering system using Django Ninja Extra."""

from datetime import date, datetime
from decimal import Decimal

from django.db.models import Q, QuerySet
from django.db.models.fields import (
    BooleanField,
    DateField,
    DateTimeField,
    DecimalField,
    IntegerField,
)
from ninja import Schema
from ninja_extra.schemas import FilterSchema
from pydantic import Field


class BaseSearchFilter(FilterSchema):
    """Base search filter with common search functionality."""

    search: str | None = Field(None, description="Search term to filter results")
    ordering: str | None = Field(
        None, description="Field to order by (use - prefix for descending)"
    )
    limit: int | None = Field(
        20, description="Maximum number of results to return", le=100
    )
    offset: int | None = Field(0, description="Number of results to skip", ge=0)


class DateRangeFilter(Schema):
    """Date range filtering."""

    date_from: date | None = Field(None, description="Start date (YYYY-MM-DD)")
    date_to: date | None = Field(None, description="End date (YYYY-MM-DD)")


class DateTimeRangeFilter(Schema):
    """DateTime range filtering."""

    datetime_from: datetime | None = Field(
        None, description="Start datetime (ISO format)"
    )
    datetime_to: datetime | None = Field(None, description="End datetime (ISO format)")


class PriceRangeFilter(Schema):
    """Price range filtering."""

    price_min: Decimal | None = Field(None, description="Minimum price", ge=0)
    price_max: Decimal | None = Field(None, description="Maximum price", ge=0)


class UserSearchFilter(BaseSearchFilter):
    """Advanced search filter for users."""

    is_staff: bool | None = Field(None, description="Filter by staff status")
    is_superuser: bool | None = Field(None, description="Filter by superuser status")
    is_active: bool | None = Field(None, description="Filter by active status")
    role: str | None = Field(None, description="Filter by role name")
    email_domain: str | None = Field(None, description="Filter by email domain")
    created_after: date | None = Field(None, description="Created after date")
    created_before: date | None = Field(None, description="Created before date")

    class Config:
        extra = "forbid"


class ProductSearchFilter(BaseSearchFilter):
    """Advanced search filter for products."""

    category: str | None = Field(None, description="Filter by category slug")
    brand: str | None = Field(None, description="Filter by brand slug")
    is_active: bool | None = Field(None, description="Filter by active status")
    is_featured: bool | None = Field(None, description="Filter by featured status")
    in_stock: bool | None = Field(None, description="Filter by stock availability")
    price_min: Decimal | None = Field(None, description="Minimum price", ge=0)
    price_max: Decimal | None = Field(None, description="Maximum price", ge=0)
    rating_min: float | None = Field(None, description="Minimum rating", ge=0, le=5)
    tags: list[str] | None = Field(None, description="Filter by tags")
    sku: str | None = Field(None, description="Filter by SKU")

    class Config:
        extra = "forbid"


class OrderSearchFilter(BaseSearchFilter):
    """Advanced search filter for orders."""

    status: str | None = Field(None, description="Filter by order status")
    payment_status: str | None = Field(None, description="Filter by payment status")
    customer_id: str | None = Field(None, description="Filter by customer ID")
    customer_email: str | None = Field(None, description="Filter by customer email")
    total_min: Decimal | None = Field(None, description="Minimum order total", ge=0)
    total_max: Decimal | None = Field(None, description="Maximum order total", ge=0)
    created_after: date | None = Field(None, description="Created after date")
    created_before: date | None = Field(None, description="Created before date")
    shipping_country: str | None = Field(None, description="Filter by shipping country")

    class Config:
        extra = "forbid"


class CustomerSearchFilter(BaseSearchFilter):
    """Advanced search filter for customers."""

    is_active: bool | None = Field(None, description="Filter by active status")
    customer_group: str | None = Field(None, description="Filter by customer group")
    country: str | None = Field(None, description="Filter by country")
    city: str | None = Field(None, description="Filter by city")
    phone: str | None = Field(None, description="Filter by phone number")
    created_after: date | None = Field(None, description="Created after date")
    created_before: date | None = Field(None, description="Created before date")
    has_orders: bool | None = Field(
        None, description="Filter by whether customer has orders"
    )

    class Config:
        extra = "forbid"


class AdvancedSearchEngine:
    """Advanced search engine with intelligent filtering and search capabilities."""

    def __init__(self, model_class, search_fields: list[str] = None):
        """Initialize search engine for a model.

        Args:
            model_class: Django model class to search
            search_fields: List of fields to include in text search
        """
        self.model_class = model_class
        self.search_fields = search_fields or []

    def apply_search(self, queryset: QuerySet, filters: BaseSearchFilter) -> QuerySet:
        """Apply search and filtering to queryset."""
        # Apply text search
        if filters.search and self.search_fields:
            queryset = self._apply_text_search(queryset, filters.search)

        # Apply specific filters based on filter type
        queryset = self._apply_specific_filters(queryset, filters)

        # Apply ordering
        if filters.ordering:
            queryset = self._apply_ordering(queryset, filters.ordering)

        return queryset

    def _apply_text_search(self, queryset: QuerySet, search_term: str) -> QuerySet:
        """Apply intelligent text search across multiple fields."""
        if not search_term.strip():
            return queryset

        # Split search term into words for better matching
        search_words = [word.strip() for word in search_term.split() if word.strip()]

        # Build search query
        search_query = Q()

        for word in search_words:
            word_query = Q()

            for field in self.search_fields:
                # Handle related field searches (e.g., 'user__username')
                if "__" in field:
                    word_query |= Q(**{f"{field}__icontains": word})
                else:
                    # Try different search patterns
                    field_obj = self.model_class._meta.get_field(field.split("__")[0])

                    if isinstance(field_obj, (DateField, DateTimeField)):
                        # For date fields, try exact match if it looks like a date
                        try:
                            date_value = datetime.strptime(word, "%Y-%m-%d").date()
                            word_query |= Q(**{field: date_value})
                        except ValueError:
                            pass
                    elif isinstance(field_obj, BooleanField):
                        # For boolean fields, try to match true/false variations
                        if word.lower() in ["true", "1", "yes", "active", "enabled"]:
                            word_query |= Q(**{field: True})
                        elif word.lower() in [
                            "false",
                            "0",
                            "no",
                            "inactive",
                            "disabled",
                        ]:
                            word_query |= Q(**{field: False})
                    elif isinstance(field_obj, (DecimalField, IntegerField)):
                        # For numeric fields, try exact match
                        try:
                            numeric_value = float(word)
                            word_query |= Q(**{field: numeric_value})
                        except ValueError:
                            pass
                    else:
                        # Default text search with various patterns
                        word_query |= Q(**{f"{field}__icontains": word})
                        word_query |= Q(**{f"{field}__istartswith": word})

            search_query &= word_query

        return queryset.filter(search_query)

    def _apply_specific_filters(
        self, queryset: QuerySet, filters: BaseSearchFilter
    ) -> QuerySet:
        """Apply model-specific filters."""
        if isinstance(filters, UserSearchFilter):
            return self._apply_user_filters(queryset, filters)
        if isinstance(filters, ProductSearchFilter):
            return self._apply_product_filters(queryset, filters)
        if isinstance(filters, OrderSearchFilter):
            return self._apply_order_filters(queryset, filters)
        if isinstance(filters, CustomerSearchFilter):
            return self._apply_customer_filters(queryset, filters)

        return queryset

    def _apply_user_filters(
        self, queryset: QuerySet, filters: UserSearchFilter
    ) -> QuerySet:
        """Apply user-specific filters."""
        if filters.is_staff is not None:
            queryset = queryset.filter(is_staff=filters.is_staff)

        if filters.is_superuser is not None:
            queryset = queryset.filter(is_superuser=filters.is_superuser)

        if filters.is_active is not None:
            queryset = queryset.filter(is_active=filters.is_active)

        if filters.role:
            queryset = queryset.filter(
                user_roles__role__name=filters.role, user_roles__is_active=True
            )

        if filters.email_domain:
            queryset = queryset.filter(email__icontains=f"@{filters.email_domain}")

        if filters.created_after:
            queryset = queryset.filter(date_joined__date__gte=filters.created_after)

        if filters.created_before:
            queryset = queryset.filter(date_joined__date__lte=filters.created_before)

        return queryset

    def _apply_product_filters(
        self, queryset: QuerySet, filters: ProductSearchFilter
    ) -> QuerySet:
        """Apply product-specific filters."""
        if filters.category:
            queryset = queryset.filter(category__slug=filters.category)

        if filters.brand:
            queryset = queryset.filter(brand__slug=filters.brand)

        if filters.is_active is not None:
            queryset = queryset.filter(is_active=filters.is_active)

        if filters.is_featured is not None:
            queryset = queryset.filter(is_featured=filters.is_featured)

        if filters.in_stock is not None:
            if filters.in_stock:
                queryset = queryset.filter(inventory__quantity__gt=0)
            else:
                queryset = queryset.filter(inventory__quantity=0)

        if filters.price_min is not None:
            queryset = queryset.filter(price__gte=filters.price_min)

        if filters.price_max is not None:
            queryset = queryset.filter(price__lte=filters.price_max)

        if filters.rating_min is not None:
            queryset = queryset.filter(average_rating__gte=filters.rating_min)

        if filters.tags:
            for tag in filters.tags:
                queryset = queryset.filter(tags__name__icontains=tag)

        if filters.sku:
            queryset = queryset.filter(sku__icontains=filters.sku)

        return queryset

    def _apply_order_filters(
        self, queryset: QuerySet, filters: OrderSearchFilter
    ) -> QuerySet:
        """Apply order-specific filters."""
        if filters.status:
            queryset = queryset.filter(status=filters.status)

        if filters.payment_status:
            queryset = queryset.filter(payment__status=filters.payment_status)

        if filters.customer_id:
            queryset = queryset.filter(customer__id=filters.customer_id)

        if filters.customer_email:
            queryset = queryset.filter(
                customer__user__email__icontains=filters.customer_email
            )

        if filters.total_min is not None:
            queryset = queryset.filter(total__gte=filters.total_min)

        if filters.total_max is not None:
            queryset = queryset.filter(total__lte=filters.total_max)

        if filters.created_after:
            queryset = queryset.filter(created_at__date__gte=filters.created_after)

        if filters.created_before:
            queryset = queryset.filter(created_at__date__lte=filters.created_before)

        if filters.shipping_country:
            queryset = queryset.filter(
                shipping_address__country=filters.shipping_country
            )

        return queryset

    def _apply_customer_filters(
        self, queryset: QuerySet, filters: CustomerSearchFilter
    ) -> QuerySet:
        """Apply customer-specific filters."""
        if filters.is_active is not None:
            queryset = queryset.filter(is_active=filters.is_active)

        if filters.customer_group:
            queryset = queryset.filter(customer_group__name=filters.customer_group)

        if filters.country:
            queryset = queryset.filter(addresses__country=filters.country)

        if filters.city:
            queryset = queryset.filter(addresses__city__icontains=filters.city)

        if filters.phone:
            queryset = queryset.filter(phone__icontains=filters.phone)

        if filters.created_after:
            queryset = queryset.filter(created_at__date__gte=filters.created_after)

        if filters.created_before:
            queryset = queryset.filter(created_at__date__lte=filters.created_before)

        if filters.has_orders is not None:
            if filters.has_orders:
                queryset = queryset.filter(orders__isnull=False)
            else:
                queryset = queryset.filter(orders__isnull=True)

        return queryset.distinct()

    def _apply_ordering(self, queryset: QuerySet, ordering: str) -> QuerySet:
        """Apply ordering to queryset with validation."""
        # Get valid field names for the model
        valid_fields = [field.name for field in self.model_class._meta.get_fields()]

        # Parse ordering (handle - prefix for descending)
        order_fields = []
        for field in ordering.split(","):
            field = field.strip()
            if field.startswith("-"):
                field_name = field[1:]
                if field_name in valid_fields:
                    order_fields.append(field)
            elif field in valid_fields:
                order_fields.append(field)

        if order_fields:
            queryset = queryset.order_by(*order_fields)

        return queryset


def create_search_engine(model_class, search_fields: list[str]) -> AdvancedSearchEngine:
    """Factory function to create a search engine for a model."""
    return AdvancedSearchEngine(model_class, search_fields)


# Pre-configured search engines for common models
def get_user_search_engine():
    """Get search engine for User model."""
    search_fields = ["username", "email", "first_name", "last_name"]
    from core.models import User

    return create_search_engine(User, search_fields)


def get_product_search_engine():
    """Get search engine for Product model."""
    search_fields = [
        "name",
        "description",
        "sku",
        "brand__name",
        "category__name",
        "tags__name",
    ]
    from products.models import Product

    return create_search_engine(Product, search_fields)


def get_order_search_engine():
    """Get search engine for Order model."""
    search_fields = [
        "order_number",
        "customer__user__email",
        "customer__user__first_name",
        "customer__user__last_name",
        "status",
        "shipping_address__country",
    ]
    from orders.models import Order

    return create_search_engine(Order, search_fields)


def get_customer_search_engine():
    """Get search engine for Customer model."""
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone",
        "addresses__city",
        "addresses__country",
    ]
    from core.models import Customer

    return create_search_engine(Customer, search_fields)
