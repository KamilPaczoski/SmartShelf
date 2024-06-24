import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from OpenAI.models import TextToSpeech
from OpenAI.text_speech import text_to_speech
from OpenAI.moderation import increase_penalty_count, content_check
from accounts.models import Penalty
from .forms import ReviewForm
from .models import Book, Rating, Shelf
from .models import Review


@login_required
def user_shelf(request):
    user = request.user
    shelf_types = ['read_later', 'favourite', 'rated']
    context = {'placeholder_img': '/static/images/book_cover_placeholder.png'}

    for shelf_type in shelf_types:
        if shelf_type != 'rated':
            books = Shelf.objects.filter(user=user, shelf_type=shelf_type).select_related('book')
        else:
            books = Rating.objects.filter(user=user).select_related('book')

        placeholder_books_count = max(0, 6 - books.count())
        placeholder_books = [Book(title='Placeholder', img=context['placeholder_img'])] * placeholder_books_count
        books = list(books) + placeholder_books

        context[shelf_type] = books

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
    reviews = Review.objects.filter(book=book)
    user_rating = Rating.objects.filter(user=request.user, book=book).first()
    read_later = Shelf.objects.filter(user=request.user, book=book, shelf_type='read_later').exists()
    favourite = Shelf.objects.filter(user=request.user, book=book, shelf_type='favourite').exists()
    user_penalties = Penalty.objects.filter(user=request.user)
    tts = TextToSpeech.objects.filter(book=book).first()

    red_penalty_count = \
        user_penalties.filter(category__in=['hate', 'self-harm/instructions', 'harassment/threatening']).aggregate(
            count=Sum('count'))['count'] or 0
    if red_penalty_count >= 10:
        cannot_post_reviews = True
    else:
        cannot_post_reviews = False
    if request.method == 'POST':
        if 'rating' in request.POST:
            Rating.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'rating': float(request.POST.get('rating'))}
            )
            book.update_rating()
        elif not cannot_post_reviews and (form := ReviewForm(request.POST)).is_valid() and (
                content := form.cleaned_data.get('content')):
            moderation_result = content_check(content)
            increase_penalty_count(request.user, moderation_result['categories'])
            if not moderation_result['block']:
                Review.objects.create(user=request.user, book=book, content=content)
        return redirect('book_detail', pk=book.pk)
    else:
        form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
        'user_rating': user_rating,
        'read_later': read_later,
        'favourite': favourite,
        'cannot_post_reviews': cannot_post_reviews,
        'penalties': user_penalties,
        'tts': tts,
    }

    return render(request, 'book_detail.html', context)


@login_required
def add_to_shelf(request, pk, shelf_type):
    book = get_object_or_404(Book, pk=pk)
    shelf, created = Shelf.objects.get_or_create(user=request.user, book=book, shelf_type=shelf_type)
    if not created:
        shelf.delete()
    return redirect('book_detail', pk=pk)


@csrf_exempt
@login_required
def generate_speech(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        voice = data.get('voice')
        book = get_object_or_404(Book, pk=pk)
        tts, _ = TextToSpeech.objects.get_or_create(book=book)
        try:
            filename = text_to_speech(book.desc, voice)
            setattr(tts, f'{voice}_audio', f'{voice}/{filename}')
            tts.save()
            return JsonResponse({'success': True})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})
