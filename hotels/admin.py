from django.contrib import admin
from django.utils.html import format_html
from .models import Hotel, Room, Booking
from django.urls import path
from django.shortcuts import render

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner', 'total_bookings', 'display_image')
    search_fields = ('name', 'location')
    list_filter = ('location',)
    fields = ('name', 'location', 'owner', 'description', 'image')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    
    display_image.short_description = "Hotel Image"

    def total_bookings(self, obj):
        return obj.rooms.filter(booking__isnull=False).count()
    
    total_bookings.short_description = "Total Bookings"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'price_per_night', 'is_available', 'total_revenue', 'display_image')
    list_filter = ('hotel', 'room_type', 'is_available')
    search_fields = ('hotel__name', 'room_type')
    fields = ('hotel', 'room_type', 'price_per_night', 'is_available', 'image')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    
    display_image.short_description = "Room Image"

    def total_revenue(self, obj):
        total = sum(booking.total_price for booking in obj.booking_set.all())
        return f"₹{total}"
    
    total_revenue.short_description = "Total Revenue"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_room_type', 'get_hotel', 'check_in', 'check_out', 'total_price')
    list_filter = ('room__hotel', 'check_in')
    search_fields = ('user__username', 'room__hotel__name')
    readonly_fields = ('total_price',)

    def get_room_type(self, obj):
        return obj.room.room_type
    get_room_type.short_description = "Room Type"

    def get_hotel(self, obj):
        return obj.room.hotel.name
    get_hotel.short_description = "Hotel"