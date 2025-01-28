from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from core.models import CustomerFeedback

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ["username", "email", "id", "is_staff"]
    search_fields = ["username", "email"]
    list_filter = ["is_staff"]


@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(ModelAdmin):
    list_display = ["id", "customer", "feedback", "rating", "created_at"]
    search_fields = ["customer__username", "feedback"]
    list_filter = ["rating"]
    ordering = ["-created_at"]
