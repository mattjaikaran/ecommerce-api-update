# Generated by Django 5.1.4 on 2025-02-12 05:06

import core.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("username", models.CharField(max_length=50, unique=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "ordering": ["-date_joined"],
            },
            managers=[
                ("objects", core.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("address_line_1", models.CharField(max_length=255)),
                (
                    "address_line_2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("zip_code", models.CharField(max_length=255)),
                ("country", models.CharField(max_length=255)),
                ("phone", models.CharField(max_length=255)),
                ("is_default", models.BooleanField(default=False)),
                ("is_billing", models.BooleanField(default=False)),
                ("is_shipping", models.BooleanField(default=False)),
                ("is_shipping_default", models.BooleanField(default=False)),
                ("is_billing_default", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_deleted",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Address",
                "verbose_name_plural": "Addresses",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("phone", models.CharField(max_length=255)),
                ("is_default", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_deleted",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer",
                "verbose_name_plural": "Customers",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CustomerFeedback",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("feedback", models.TextField(max_length=500)),
                (
                    "rating",
                    models.IntegerField(
                        choices=[
                            (1, "1 Star"),
                            (2, "2 Stars"),
                            (3, "3 Stars"),
                            (4, "4 Stars"),
                            (5, "5 Stars"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customer_feedback",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_deleted",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer Feedback",
                "verbose_name_plural": "Customer Feedback Messages",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CustomerGroup",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "customers",
                    models.ManyToManyField(
                        related_name="customer_groups", to="core.customer"
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_deleted",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer Group",
                "verbose_name_plural": "Customer Groups",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OneTimePassword",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField()),
                ("is_used", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
