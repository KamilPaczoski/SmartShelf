from rest_framework import viewsets, generics
from .models import Book, Rating, Comment, Shelf
from .serializers import BookSerializer, RatingSerializer, CommentSerializer, ShelfSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
