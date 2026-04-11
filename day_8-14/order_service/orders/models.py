from django.db import models


class Order(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    status_choices = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.id} - Product {self.product_id}"
