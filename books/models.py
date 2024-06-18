from django.db import models
from django.conf import settings
from django.db.models import Avg, Count

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    bookformat = models.CharField(max_length=50)
    desc = models.TextField()
    genre = models.CharField(max_length=200)
    img = models.URLField()
    isbn = models.CharField(max_length=13)
    pages = models.IntegerField()
    totalratings = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        ratings = Rating.objects.filter(book=self).aggregate(Avg('rating'), Count('rating'))
        self.rating = ratings['rating__avg'] or 0
        self.totalratings = ratings['rating__count'] or 0
        self.save()

    def __str__(self):
        return self.title

class Shelf(models.Model):
    SHELF_TYPES = [
        ('read_later', 'Read Later'),
        ('favourite', 'Favourite'),
        ('rated', 'Rated')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shelf_type = models.CharField(max_length=50, choices=SHELF_TYPES)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.shelf_type})"

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    rating = models.FloatField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating})"
