from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='../media/user_avatars/', null=True, blank=True,
                               default='../static/images/default_avatar.webp')
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='customuser_set',  # Unique related_name for CustomUser
    #     blank=True,
    #     help_text=('The groups this user belongs to. A user will get all permissions '
    #                'granted to each of their groups.'),
    #     related_query_name='customuser',
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='customuser_set',  # Unique related_name for CustomUser
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     related_query_name='customuser',
    # )
