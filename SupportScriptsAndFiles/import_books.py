import os
import sys
import django
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartshelf.settings')
django.setup()

from books.models import Book

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, 'top_200_books.csv')

df = pd.read_csv(csv_file)

df.columns = [
    'author', 'bookformat', 'desc', 'genre', 'img', 'isbn', 'pages',
    'rating', 'reviews', 'title', 'totalratings'
]
print(df['title'].str.len().max())
print(df['author'].str.len().max())
print(df['genre'].str.len().max())

for _, row in df.iterrows():
    Book.objects.get_or_create(
        title=row['title'],
        author=row['author'],
        defaults={
            'bookformat': row['bookformat'],
            'desc': row['desc'],
            'genre': row['genre'],
            'img': row['img'],
            'isbn': row['isbn'],
            'pages': row['pages'],
            'totalratings': row['totalratings'],
            'rating': row['rating']
        }
    )

print("Data imported successfully.")
