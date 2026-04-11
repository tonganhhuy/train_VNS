from django.db import models


class Cart(models.Model):
    user_id = models.IntegerField(null=True, blank=True)  # Liên kết Auth Service
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product_id = models.IntegerField()  # Tham chiếu tới Product ID bên Inventory Service
    quantity = models.PositiveIntegerField(default=1)
    price_at_addition = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Lưu giữ giá lúc thêm vào giỏ

    def __str__(self):
        return f"{self.quantity} x Product {self.product_id}"
