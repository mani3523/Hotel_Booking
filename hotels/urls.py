from django.urls import path
from .views import *


urlpatterns = [
    path('', hotel_list, name='hotel_list'),
    path('<int:hotel_id>/', hotel_detail, name='hotel_detail'),
    path('book_room/<int:room_id>/', book_room, name='book_room'),
    path('my_bookings/', my_bookings, name='my_bookings'),
    path("initiate_payment/<int:booking_id>/", initiate_payment, name="initiate_payment"),
    path("payment_success/", payment_success, name="payment_success"), 
    path('hotel_admin/', hotel_admin_dashboard, name='hotel_admin_dashboard'),   
]