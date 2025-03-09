from django.contrib import admin
from .models import Restaurant, FoodItem, Order

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner')
    search_fields = ('name', 'location', 'owner__username')  # Search by name, location, and owner
    list_filter = ('location',)  # Filter by location

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    search_fields = ('name', 'restaurant__name')  # Search by food name and restaurant name
    list_filter = ('restaurant', 'price')  # Filter by restaurant and price range

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity', 'total_price', 'created_at')
    search_fields = ('user__username', 'food_item__name')  # Search orders by user and food item
    list_filter = ('created_at', 'food_item')  # Filter orders by date and food item
    readonly_fields = ('total_price', 'created_at')  # Prevent accidental modification
