from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Shelf, Review, Rating
from accounts.models import CustomUser
from django.db.models import Q
from .forms import ReviewForm
from django.db import IntegrityError


@login_required
def user_shelf(request):
    read_later = list(Shelf.objects.filter(user=request.user, shelf_type='read_later'))
    favourite = list(Shelf.objects.filter(user=request.user, shelf_type='favourite'))
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
    favourite = fill_placeholders(favourite)
    rated = fill_placeholders(rated)

    return render(request, 'user_shelf.html', {
        'read_later': read_later,
        'favourite': favourite,
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
    reviews = Review.objects.filter(book=book).order_by('-date_posted')
    user_rating = Rating.objects.filter(user=request.user, book=book).first()

    if request.method == 'POST':
        if 'rating' in request.POST:
            rating_value = float(request.POST.get('rating'))
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'rating': rating_value}
            )
            book.update_rating()
            return redirect('book_detail', pk=book.pk)
        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.book = book
                review.save()
                return redirect('book_detail', pk=book.pk)
    else:
        form = ReviewForm()

    return render(request, 'book_detail.html', {
        'book': book,
        'reviews': reviews,
        'form': form,
        'user_rating': user_rating
    })


@login_required
def add_to_shelf(request, pk, shelf_type):
    book = get_object_or_404(Book, pk=pk)
    Shelf.objects.create(user=request.user, book=book, shelf_type=shelf_type)
    return redirect('user_shelf')
