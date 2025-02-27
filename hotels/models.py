from django.db import models
from django.contrib.auth import get_user_model
from datetime import date
from django.conf import settings
from datetime import datetime

User = get_user_model()

# Create your models here.
# Hotel Model
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hotels")  # Hotel admin
    description = models.TextField()
    image = models.ImageField(upload_to="hotel_images/", blank=True, null=True)

    def __str__(self):
        return self.name

# Room Model
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_type = models.CharField(max_length=100, choices=[("Single", "Single"), ("Double", "Double"), ("Suite", "Suite")])
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from datetime import datetime

        if isinstance(self.check_in, str):
            self.check_in = datetime.strptime(self.check_in, "%Y-%m-%d").date()
        if isinstance(self.check_out, str):
            self.check_out = datetime.strptime(self.check_out, "%Y-%m-%d").date()

        # Ensure check-out date is after check-in date
        if self.check_out > self.check_in:
            nights = (self.check_out - self.check_in).days
            self.total_price = nights * self.room.price_per_night
        else:
            self.total_price = 0  # Invalid date selection

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room.hotel.name} - {self.room.room_type}"
    

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username}"