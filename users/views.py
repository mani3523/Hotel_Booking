from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_backends
from .forms import UserRegisterForm
from django.contrib import messages

# Create your views here.
# User Registration View
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            
            user.backend = get_backends()[0].__module__ + '.' + get_backends()[0].__class__.__name__

            login(request, user)  # Now Django knows which backend to use
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")  # Redirect to login page
        else:
            messages.error(request, "Registration failed. Please check your input.")  # General error message
    else:
        form = UserRegisterForm()
    
    return render(request, "users/register.html", {"form": form})

# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Redirect to home after login
    return render(request, 'users/login.html')

# User Logout View
def user_logout(request):
    logout(request)
    return render(request, 'users/logout.html')