from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from .models import Restaurant, FoodItem, Order, RestaurantAdminAccess

User = get_user_model()


# RestaurantAdmin Panel
class RestaurantAdminPanel(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner', 'display_image')
    search_fields = ('name', 'location', 'owner__username')
    list_filter = ('location',)
    fields = ('name', 'location', 'owner', 'image')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    
    display_image.short_description = "Restaurant Image"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_authenticated:  # Prevent AnonymousUser access
            return Restaurant.objects.none()
        if request.user.is_superuser:
            return qs
        restaurant_admin = RestaurantAdminAccess.objects.filter(user=request.user).first()
        if restaurant_admin:
            return qs.filter(id=restaurant_admin.restaurant.id)
        return Restaurant.objects.none()

    def has_module_permission(self, request):
        return request.user.is_authenticated and (request.user.is_superuser or RestaurantAdminAccess.objects.filter(user=request.user).exists())

    def has_change_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return obj and obj.owner == request.user

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


# RestaurantAdminAccess Panel (Restricted to Super Admins)
class RestaurantAdminAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant')
    search_fields = ('user__username', 'restaurant__name')

    def has_module_permission(self, request):
        return request.user.is_authenticated and request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_authenticated and request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.is_superuser


# FoodItem Admin
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'is_available', 'display_image')
    search_fields = ('name', 'restaurant__name')
    list_filter = ('restaurant', 'is_available')
    fields = ('restaurant', 'name', 'price', 'is_available', 'image')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "No Image"

    display_image.short_description = "Food Image"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_authenticated:
            return FoodItem.objects.none()
        if request.user.is_superuser:
            return qs
        restaurant_admin = RestaurantAdminAccess.objects.filter(user=request.user).first()
        if restaurant_admin:
            return qs.filter(restaurant=restaurant_admin.restaurant)
        return FoodItem.objects.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "restaurant" and request.user.is_authenticated and not request.user.is_superuser:
            restaurant_admin = RestaurantAdminAccess.objects.filter(user=request.user).first()
            if restaurant_admin:
                kwargs["queryset"] = Restaurant.objects.filter(id=restaurant_admin.restaurant.id)
            else:
                kwargs["queryset"] = Restaurant.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_module_permission(self, request):
        return request.user.is_authenticated and (request.user.is_superuser or RestaurantAdminAccess.objects.filter(user=request.user).exists())

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        restaurant_admin = RestaurantAdminAccess.objects.filter(user=request.user).first()
        return obj and restaurant_admin and obj.restaurant == restaurant_admin.restaurant

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
    
    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)


# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_item', 'quantity', 'total_price', 'payment_option', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'payment_option')
    search_fields = ('name', 'food_item__name', 'phone')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_authenticated:
            return Order.objects.none()
        
        if request.user.is_superuser:
            return qs.only('payment_status', 'payment_option')  # Superuser sees only payment details
        
        restaurant_admin = RestaurantAdminAccess.objects.filter(user=request.user).first()
        if restaurant_admin:
            return qs.filter(food_item__restaurant=restaurant_admin.restaurant)
        
        return Order.objects.none()

    def has_module_permission(self, request):
        return request.user.is_authenticated and (
            request.user.is_superuser or RestaurantAdminAccess.objects.filter(user=request.user).exists()
        )

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True 
        
        if hasattr(request.user, "restaurant"):
            if obj and obj.food_item.restaurant.owner == request.user:
                return True  
            return False

        return False

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
    
    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)




# Register models
admin.site.register(Restaurant, RestaurantAdminPanel)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(RestaurantAdminAccess, RestaurantAdminAccessAdmin)
