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
