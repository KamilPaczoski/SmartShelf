from django.core.management.base import BaseCommand
from django.db.models import Count
from books.models import Book


class Command(BaseCommand):
    help = 'Remove duplicate books'

    def handle(self, *args, **kwargs):
        duplicates = (
            Book.objects
            .values('title', 'author')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        total = duplicates.count()

        for duplicate in duplicates:
            books = Book.objects.filter(
                title=duplicate['title'],
                author=duplicate['author']
            ).order_by('id')

            keep = books.first()
            deleted_count, _ = books.exclude(id=keep.id).delete()

            self.stdout.write(
                f"Removed {deleted_count} for {keep.title}"
            )

        self.stdout.write(self.style.SUCCESS(f"Cleaned {total}"))