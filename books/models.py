from django.db import models
from accounts.models import CustomUser


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
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.title


class Rating(models.Model):
    book = models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.FloatField(default=0)


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Shelf(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shelf_type = models.CharField(max_length=20,
                                  choices=[('read_later', 'Read Later'), ('already_read', 'Already Read'),
                                           ('rated', 'Rated')])
