import os

import pandas as pd
from sqlalchemy import create_engine

# loads the books data from the CSV file into a PostgreSQL database.
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(connection_string)

csv_file = 'top_50_books.csv'

df = pd.read_csv(csv_file)

df.columns = [
    'author', 'bookformat', 'desc', 'genre', 'img', 'isbn', 'pages',
    'rating', 'reviews', 'title', 'totalratings'
]

df.to_sql('books', engine, if_exists='replace', index=False)

print("Data imported successfully.")
