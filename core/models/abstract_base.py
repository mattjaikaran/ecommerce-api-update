"""Abstract base model definition."""

import uuid

from django.db import models

from .user import User


class AbstractBaseModel(models.Model):
    """Abstract base model with common fields for all models."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_created",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_updated",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)  # soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_deleted",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        indexes = [
            # Common indexes for all models inheriting from AbstractBaseModel
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["created_by"]),
            models.Index(fields=["updated_by"]),
            # Compound indexes for common queries
            models.Index(fields=["is_active", "is_deleted"]),
            models.Index(fields=["created_at", "is_active"]),
        ]
