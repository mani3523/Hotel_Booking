from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the correct user model dynamically

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User  # This now dynamically refers to CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered. Please use a different email.")
        return email
