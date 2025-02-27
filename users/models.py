from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    is_hotel_admin = models.BooleanField(default=False)  # Checkbox to identify hotel admins
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username