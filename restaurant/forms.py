from django import forms
from .models import FoodItem, Order

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'image']


class OrderForm(forms.ModelForm):
    is_hotel_guest = forms.BooleanField(required=False, label="Are you staying in a hotel?")

    class Meta:
        model = Order
        fields = ['name', 'phone', 'location', 'is_hotel_guest', 'hotel_name', 'hotel_location', 'room_number', 'quantity', 'payment_option']
        widgets = {
            'hotel_name': forms.TextInput(attrs={'placeholder': 'Hotel Name'}),
            'hotel_location': forms.TextInput(attrs={'placeholder': 'Hotel Location'}),
            'room_number': forms.TextInput(attrs={'placeholder': 'Room Number'}),
        }