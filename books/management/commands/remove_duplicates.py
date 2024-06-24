from django.core.management.base import BaseCommand

from books import models
from books.models import Shelf


class Command(BaseCommand):
    help = 'Remove duplicate entries in the Shelf table'

    def handle(self, *args, **kwargs):
        duplicates = Shelf.objects.values('user', 'book', 'shelf_type') \
            .annotate(count=models.Count('id')) \
            .filter(count__gt=1)

        for duplicate in duplicates:
            user = duplicate['user']
            book = duplicate['book']
            shelf_type = duplicate['shelf_type']
            entries = Shelf.objects.filter(user=user, book=book, shelf_type=shelf_type)
            entries_to_keep = entries.first()
            entries.exclude(id=entries_to_keep.id).delete()
            self.stdout.write(self.style.SUCCESS(
                'Duplicates removed.'
            ))

        self.stdout.write(self.style.SUCCESS('removed'))
