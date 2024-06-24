# SmartShelf

SmartShelf is a web application for browsing, rating, and reviewing books with integrated AI functionalities for content moderation and text-to-speech. This project is built using Django and leverages OpenAI's API for advanced features.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)

## Features

- User registration and login
- Personalized bookshelves (Read Later, Favorite, Rated)
- AI-based content moderation
- AI-based text-to-speech for book descriptions
- Search and sort books by title, author, rating, and total ratings
- System of penalties based on user reviews

## Tech Stack

- Python 11
- Django 5.0.6
- PostgreSQL
- HTML5
- CSS3
- Bootstrap
- OpenAI API
- elements of JavaScript

## Setup and Installation

### Prerequisites

- Python 11
- PostgreSQL

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/smartshelf.git
    cd smartshelf
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database, role should match the `DB_USER` and database should match the `DB_NAME` in the `.env` file. Run the following commands in the terminal to create the database and user
    ```bash
    sudo -u postgres psql
    CREATE DATABASE smartshelf;
    CREATE USER smartshelfuser WITH PASSWORD 'yourpassword';
    ALTER ROLE smartshelfuser SET client_encoding TO 'utf8';
    ALTER ROLE smartshelfuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE smartshelfuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE smartshelf TO smartshelfuser;
    \q
    ```

5. Configure environment variables:
    - Create a `.env` file in the root directory of the project and fill in the necessary variables as shown in the [Environment Variables](#environment-variables) section.

6. Apply database migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

8. Run the development server:
    ```bash
    python manage.py runserver (or python manage.py runserver --insecure if DEBUG=True)
    ```

## Environment Variables

Create a `.env` file in the root directory of your project with the following content:

```env
# Django settings
SECRET_KEY=your_secret_key
DEBUG=True 
ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Database settings
DB_NAME=smartshelf
DB_USER=smartshelfuser
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key
