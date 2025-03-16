from .models import RestaurantAdmin

def is_restaurant_admin(user, restaurant):
    return RestaurantAdmin.objects.filter(user=user, restaurant=restaurant).exists()