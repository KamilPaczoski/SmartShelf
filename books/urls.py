from django.urls import path
from .views import book_list, book_detail, user_shelf, account_settings, admin_home

urlpatterns = [

    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('shelf/', user_shelf, name='user_shelf'),
    path('admin_home/', admin_home, name='admin_home'),
    path('account/', account_settings, name='account_settings'),

]
