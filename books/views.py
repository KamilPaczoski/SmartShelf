from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from .forms import ReviewForm
from .models import Book, Rating, Shelf
from .models import Review


@login_required
def user_shelf(request):
    user = request.user
    read_later_books = Shelf.objects.filter(user=user, shelf_type='read_later').select_related('book')
    favourite_books = Shelf.objects.filter(user=user, shelf_type='favourite').select_related('book')
    rated_books = Rating.objects.filter(user=user).select_related('book')

    # Generate placeholder books if necessary
    placeholder_img = '/static/images/book_cover_placeholder.png'
    num_placeholders = max(0, 6 - read_later_books.count())
    read_later_books = list(read_later_books) + [Book(title='Placeholder', img=placeholder_img)] * num_placeholders

    num_placeholders = max(0, 6 - favourite_books.count())
    favourite_books = list(favourite_books) + [Book(title='Placeholder', img=placeholder_img)] * num_placeholders

    num_placeholders = max(0, 6 - rated_books.count())
    rated_books = list(rated_books) + [Book(title='Placeholder', img=placeholder_img)] * num_placeholders

    context = {
        'read_later': read_later_books,
        'favourite': favourite_books,
        'rated': rated_books,
        'placeholder_img': placeholder_img,
    }

    return render(request, 'user_shelf.html', context)


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
    read_later = Shelf.objects.filter(user=request.user, book=book, shelf_type='read_later').exists()
    favourite = Shelf.objects.filter(user=request.user, book=book, shelf_type='favourite').exists()

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
        'user_rating': user_rating,
        'read_later': read_later,
        'favourite': favourite
    })


@login_required
def add_to_shelf(request, pk, shelf_type):
    book = get_object_or_404(Book, pk=pk)
    shelf, created = Shelf.objects.get_or_create(user=request.user, book=book, shelf_type=shelf_type)
    if not created:
        shelf.delete()
    return redirect('book_detail', pk=pk)
