from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from core.controllers import UserController, AuthController, CustomerController
from products.controllers import (
    ProductController,
    CategoryController,
    CollectionController,
    TagController,
    ProductOptionController,
    AttributeController,
    BundleController,
    ReviewController,
)
from cart.controllers import CartController, CartItemController
from orders.controllers import OrderController
from ninja import Redoc
from debug_toolbar.toolbar import debug_toolbar_urls

# admin site settings
admin.site.site_header = "E-Commerce Admin"
admin.site.site_title = "E-Commerce Panel"
admin.site.index_title = "Welcome to E-Commerce Panel"
admin.site.site_url = "/api/docs"

api = NinjaExtraAPI(
    version="1.0.0",
    title="E-Commerce API",
    description="API documentation for the E-Commerce API",
    urls_namespace="api_v1",
    docs=Redoc(),
    auth=None,
    csrf=False,
)

# Register controllers
api.register_controllers(
    NinjaJWTDefaultController,
    UserController,
    AuthController,
    CustomerController,
    # Register specific product-related controllers first
    CategoryController,
    CollectionController,
    TagController,
    ProductOptionController,
    AttributeController,
    BundleController,
    ReviewController,
    # Register the general product controller last
    ProductController,
    CartController,
    CartItemController,
    OrderController,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
