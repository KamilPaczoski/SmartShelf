import os
from django.db import models

from books.models import Book


class TextToSpeech(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    onyx_audio = models.FileField(upload_to='onyx/', blank=True, null=True)
    nova_audio = models.FileField(upload_to='nova/', blank=True, null=True)

    def __str__(self):
        return f'TextToSpeech for {self.book.title}'

    def delete_files(self):
        if self.onyx_audio:
            os.remove(self.onyx_audio.path)
        if self.nova_audio:
            os.remove(self.nova_audio.path)