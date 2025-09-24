"""Customer feedback model definition."""

from django.db import models

from .abstract_base import AbstractBaseModel
from .user import User


class CustomerFeedback(AbstractBaseModel):
    """Model for storing customer feedback and ratings."""

    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_feedback"
    )
    feedback = models.TextField(max_length=500)
    rating = models.IntegerField(
        default=0,
        choices=[
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        ],
    )

    def __str__(self):
        return f"{self.customer.username} - {self.feedback[:50]}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer Feedback"
        verbose_name_plural = "Customer Feedback Messages"
        indexes = [
            models.Index(fields=["customer"]),
            models.Index(fields=["rating"]),
            models.Index(fields=["created_at"]),
        ]
