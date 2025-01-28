# products/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Products

@admin.register(Products)
class ProductsAdmin(ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
