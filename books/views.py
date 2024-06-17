from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Shelf
from django.db.models import Q


@login_required
def user_shelf(request):
    read_later = list(Shelf.objects.filter(user=request.user, shelf_type='read_later'))
    already_read = list(Shelf.objects.filter(user=request.user, shelf_type='already_read'))
    rated = list(Shelf.objects.filter(user=request.user, shelf_type='rated'))

    placeholder_img = '/static/images/book_cover_placeholder.png'  # Path to the placeholder image

    def fill_placeholders(shelf_list):
        while len(shelf_list) < 6:
            shelf_list.append({
                'book': {
                    'img': placeholder_img,
                    'title': 'Placeholder'
                },
                'is_placeholder': True
            })
        return shelf_list

    read_later = fill_placeholders(read_later)
    already_read = fill_placeholders(already_read)
    rated = fill_placeholders(rated)

    return render(request, 'user_shelf.html', {
        'read_later': read_later,
        'already_read': already_read,
        'rated': rated,
        'placeholder_img': placeholder_img
    })


@login_required
def account_settings(request):
    return render(request, 'account_settings.html')


@login_required
def book_list(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'title')
    books = Book.objects.all()

    if search_query:
        books = books.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))

    if sort_by == 'totalratings':
        books = books.order_by('-totalratings')
    elif sort_by == 'rating':
        books = books.order_by('-rating')
    else:
        books = books.order_by('title')

    return render(request, 'book_list.html', {'books': books, 'search_query': search_query, 'sort_by': sort_by})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    comments = book.comments_set.all()
    return render(request, 'book_detail.html', {'book': book, 'comments': comments})
