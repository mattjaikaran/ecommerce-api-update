from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from core.controllers import UserController, AuthController
from products.controllers import ProductController
from cart.controllers import CartController
from orders.controllers import OrderController
from ninja import Redoc
from debug_toolbar.toolbar import debug_toolbar_urls

# admin site settings
admin.site.site_header = "E-Commerce Admin"
admin.site.site_title = "E-Commerce Panel"
admin.site.index_title = "Welcome to E-Commerce Panel"
admin.site.site_url = "/api/docs"

# Instantiate the server
"""
normally for django-ninja it looks like - 
api = NinjaAPI()

ninja extra normally looks like -
api = NinjaExtraAPI()

Below we are adding in Swagger/OpenAPI params
seen at http://localhost:8000/api/docs
"""

api = NinjaExtraAPI(
    # csrf=True,  # this line is to enable CSRF protection
    openapi_extra={
        "info": {
            "termsOfService": "https://example.com/terms/",
        }
    },
    version=0.1,
    title="E-Commerce API",
    description="API documentation for the E-Commerce API",
    urls_namespace="ecommerce_api",
    docs=Redoc(),  # this line is to use ReDoc instead of Swagger
)


# Register controllers
# The order of the controllers matches the order in the API Docs (Swager or ReDoc)
# http://localhost:8000/api/docs
api.register_controllers(
    NinjaJWTDefaultController,  # JWT Auth. If you want to use JWT, you must include this https://github.com/eadwinCode/django-ninja-jwt
    # core app
    UserController,  # User Controller
    AuthController,  # Auth Controller
    # products app
    ProductController,  # Product Controller
    # cart app
    CartController,  # Cart Controller
    # orders app
    OrderController,  # Order Controller
    # payments app
    # reports app
)

# add the urls to the urlpatterns
urlpatterns = [
    path("admin/", admin.site.urls),
    # this includes all of the endpoints defined in the controllers (api.register_controllers)
    # and adds a /api prefix to the urls
    path("api/", api.urls),
] + debug_toolbar_urls()  # this is for the debug toolbar.

# this is for the static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
