from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import CustomerFeedback


@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(ModelAdmin):
    list_display = ["id", "customer", "feedback", "rating", "created_at"]
    search_fields = ["customer__username", "feedback"]
    list_filter = ["rating"]
    ordering = ["-created_at"]
