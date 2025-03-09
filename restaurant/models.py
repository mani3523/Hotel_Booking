from django.db import models
from django.contrib.auth import get_user_model
from hotels.models import *

User = get_user_model()

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurants")  
    image = models.ImageField(upload_to="restaurant_images/", blank=True, null=True)
    description = models.TextField(default="No description available.", null=True, blank=True)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="food_items")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="orders")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    # Customer Information
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=15, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # Address for External Users

    # Hotel Guest Details
    is_hotel_guest = models.BooleanField(default=False)
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    hotel_location = models.CharField(max_length=255, blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)

    # Payment Details
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
    ]
    payment_option = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='COD')

    # Razorpay Payment Status
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.food_item:
            self.total_price = self.food_item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order by {self.name or 'Guest'} - {self.food_item.name} ({self.quantity})"
