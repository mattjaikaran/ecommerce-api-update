# orders/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Orders

@admin.register(Orders)
class OrdersAdmin(ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
