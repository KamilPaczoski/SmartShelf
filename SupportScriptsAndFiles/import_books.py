import os
import django
import pandas as pd
from books.models import Book

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartshelf.settings')
django.setup()

csv_file = 'top_200_books.csv'
df = pd.read_csv(csv_file)

print(df.head())
df.columns = [
    'author', 'bookformat', 'desc', 'genre', 'img', 'isbn', 'pages',
    'rating', 'reviews', 'title', 'totalratings'
]

for index, row in df.iterrows():
    Book.objects.create(
        title=row['title'],
        author=row['author'],
        bookformat=row['bookformat'],
        desc=row['desc'],
        genre=row['genre'],
        img=row['img'],
        isbn=row['isbn'],
        pages=row['pages'],
        totalratings=row['totalratings'],
        rating=row['rating']
    )

print("Data imported successfully.")
