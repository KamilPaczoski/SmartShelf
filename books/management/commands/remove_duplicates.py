from django.core.management.base import BaseCommand
from django.db.models import Count
from books.models import Shelf


class Command(BaseCommand):
    help = 'Remove duplicate entries in the Shelf table'

    def handle(self, *args, **kwargs):
        duplicates = (
            Shelf.objects
            .values('user', 'book', 'shelf_type')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        for duplicate in duplicates:
            entries = Shelf.objects.filter(
                user=duplicate['user'],
                book=duplicate['book'],
                shelf_type=duplicate['shelf_type']
            )

            keep = entries.first()
            entries.exclude(id=keep.id).delete()

        self.stdout.write(self.style.SUCCESS('✅ Duplicates removed'))