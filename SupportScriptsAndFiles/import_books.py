import os
import django
import pandas as pd

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartshelf.settings')

# Initialize Django
django.setup()

# Import the Book model after setting up Django
from books.models import Book

# Read the CSV file
csv_file = 'top_200_books.csv'
df = pd.read_csv(csv_file)

# Inspect the DataFrame
print(df.head())

# Rename the columns to match the database schema if necessary
df.columns = [
    'author', 'bookformat', 'desc', 'genre', 'img', 'isbn', 'pages',
    'rating', 'reviews', 'title', 'totalratings'
]

# Import data into the database using Django ORM
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
