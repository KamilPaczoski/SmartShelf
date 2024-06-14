from django.db import models
from accounts.models import CustomUser


class Book(models.Model):
    title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='covers/')
    description = models.TextField()
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    pages = models.IntegerField()
    format = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13)


class Rating(models.Model):
    book = models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.FloatField()


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
