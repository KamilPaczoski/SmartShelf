from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import os


def user_avatar_path(instance, filename):
    # Generate a random unique token
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('user_avatars', filename)


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True, default='images/default_avatar.webp')
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)


class Penalty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} - {self.category} - {self.count}'
