from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from .models import Hotel, Room, Booking, HotelAdmin as HotelAdminModel

User = get_user_model()

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
    
    def get_queryset(self, request):
        """Ensure hotel admins see only their assigned hotel."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'hoteladmin'):
            return qs.filter(owner=request.user)  # Restrict hotel admins to their assigned hotel
        return Hotel.objects.none()

    def has_module_permission(self, request):
        """Show Hotels menu only if user has access."""
        return request.user.is_superuser or hasattr(request.user, 'hoteladmin')

    def has_change_permission(self, request, obj=None):
        """Allow editing only assigned hotel."""
        if request.user.is_superuser:
            return True
        return obj is not None and obj.owner == request.user
    

    def has_delete_permission(self, request, obj=None):
        """Allow deleting only assigned hotel."""
        return self.has_change_permission(request, obj)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('hotel', 'room_type', 'is_available')
    search_fields = ('hotel__name', 'room_type')
    fields = ('hotel', 'room_type', 'price_per_night', 'is_available', 'image')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all rooms
        try:
            hotel_admin = HotelAdminModel.objects.get(user=request.user)
            return qs.filter(hotel=hotel_admin.hotel)  # Show only rooms for their hotel
        except HotelAdminModel.DoesNotExist:
            return qs.none()  # No rooms if not assigned to a hotel

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "hotel" and not request.user.is_superuser:
            try:
                hotel_admin = HotelAdminModel.objects.get(user=request.user)
                kwargs["queryset"] = Hotel.objects.filter(id=hotel_admin.hotel.id)  # Restrict selection to their hotel
            except HotelAdminModel.DoesNotExist:
                kwargs["queryset"] = Hotel.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



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

    def get_queryset(self, request):
        """Ensure hotel admins see only bookings for their assigned hotel."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'hoteladmin'):
            return qs.filter(room__hotel=request.user.hoteladmin.hotel)  # Restrict to assigned hotel's bookings
        return Booking.objects.none()

    def has_module_permission(self, request):
        """Show Bookings menu only if user has access."""
        return request.user.is_superuser or hasattr(request.user, 'hoteladmin')

    def has_change_permission(self, request, obj=None):
        """Allow editing only bookings of assigned hotel."""
        if request.user.is_superuser:
            return True
        return obj is not None and obj.room.hotel.owner == request.user

    def has_delete_permission(self, request, obj=None):
        """Allow deleting only bookings of assigned hotel."""
        return self.has_change_permission(request, obj)


@admin.register(HotelAdminModel)
class HotelAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel')


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
