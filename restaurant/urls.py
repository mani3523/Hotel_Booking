from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('order/<int:food_id>/', views.order_food, name='order_food'),
    path('add_food/<int:restaurant_id>/', views.add_food_item, name='add_food_item'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_success/', views.order_success, name='order_success'),
]