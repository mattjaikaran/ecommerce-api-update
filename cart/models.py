from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import AbstractBaseModel
from products.models import ProductVariant


class Cart(AbstractBaseModel):
    session_key = models.CharField(max_length=255, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Cart {self.id}"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(AbstractBaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_variant.product.name}"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
