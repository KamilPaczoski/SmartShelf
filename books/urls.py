from django.urls import path
from .views import book_list, book_detail, user_shelf, account_settings

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('shelf/', user_shelf, name='user_shelf'),
    path('account/', account_settings, name='account_settings'),
]
