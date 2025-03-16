from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('terms_and_conditions/', terms_and_conditions, name='terms_and_conditions'),
]
