from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login_register/', views.login_register, name='login_register'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login_register/'), name='logout'),
]