from django.urls import path
from .views import login_register, account_settings, delete_account

urlpatterns = [
    path('login_register/', login_register, name='login_register'),
    path('account_settings/', account_settings, name='account_settings'),
    path('delete_account/', delete_account, name='delete_account'),
]
