from django.urls import path
from .views import login_register

urlpatterns = [
    path('login_register/', login_register, name='login_register'),
]
