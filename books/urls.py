from django.urls import path
from .views import user_shelf, account_settings, book_list, book_detail

urlpatterns = [
    path('shelf/', user_shelf, name='user_shelf'),
    path('account/', account_settings, name='account_settings'),
    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
]
