from django.shortcuts import render, get_object_or_404
from .models import Book, Shelf


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    comments = book.comments_set.all()
    return render(request, 'book_detail.html', {'book': book, 'comments': comments})


def user_shelf(request):
    read_later = Shelf.objects.filter(user=request.user, shelf_type='read_later')
    already_read = Shelf.objects.filter(user=request.user, shelf_type='already_read')
    rated = Shelf.objects.filter(user=request.user, shelf_type='rated')
    return render(request, 'user_shelf.html', {'read_later': read_later, 'already_read': already_read, 'rated': rated})


def account_settings(request):
    return render(request, 'account_settings.html')
