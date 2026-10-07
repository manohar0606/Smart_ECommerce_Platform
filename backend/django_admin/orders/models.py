from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )

    ORDER_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
    )
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default="pending",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        unique_together = ("order", "product")

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ("stripe", "Stripe"),
        ("card", "Card"),
        ("other", "Other"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="stripe",
    )
    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ("order", "Order"),
        ("shipping", "Shipping"),
        ("payment", "Payment"),
        ("general", "General"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
        default="general",
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"