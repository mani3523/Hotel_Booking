from django import forms
from .models import FoodItem, Order

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'price', 'description', 'is_available', 'image']


class OrderForm(forms.ModelForm):
    is_hotel_guest = forms.BooleanField(required=False, label="Are you staying in a hotel?")

    class Meta:
        model = Order
        fields = ['name', 'phone', 'location', 'is_hotel_guest', 'hotel_name', 'hotel_location', 'room_number', 'payment_option']
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['hotel_name'].required = False
        self.fields['hotel_location'].required = False
        self.fields['room_number'].required = False

    class Meta:
        model = Order
        fields = ['name', 'phone', 'location', 'is_hotel_guest', 'hotel_name', 'hotel_location', 'room_number', 'quantity', 'payment_option']
        widgets = {
            'hotel_name': forms.TextInput(attrs={'placeholder': 'Hotel Name'}),
            'hotel_location': forms.TextInput(attrs={'placeholder': 'Hotel Location'}),
            'room_number': forms.TextInput(attrs={'placeholder': 'Room Number'}),
        }