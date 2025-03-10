from .models import HotelAdmin

def is_hotel_admin(user, hotel):
    return HotelAdmin.objects.filter(user=user, hotel=hotel).exists()
