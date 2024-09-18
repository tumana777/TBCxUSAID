from faker import Faker
import random
import sqlite3
from datetime import datetime

fake = Faker()

# Manually create book genres
genres = [
    "Fantasy", "Science Fiction", "Mystery", "Thriller", "Romance", "Historical Fiction", "Horror",
    "Young Adult (YA)", "Dystopian", "Adventure", "Literary Fiction", "Non-Fiction",
    "Biography/Autobiography", "Self-Help", "Philosophical Fiction", "Poetry", "Magical Realism",
    "Crime", "Urban Fantasy", "Epic Fantasy", "Political Fiction", "Psychological Thriller", "Western",
    "Chick Lit", "Graphic Novel", "Paranormal Romance", "Suspense", "Legal Thriller", "Satire", "Travel"
]

min_age = 12

# Get the current year
current_year = datetime.now().year

# Generate fake authors
authors = [(fake.first_name(), fake.last_name(), fake.date_of_birth(None, min_age), fake.country()) for _ in range(500)]

# Establish connection to database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# This is for enabling foreign key
cursor.execute('PRAGMA foreign_keys = ON;')

# Create authors table in database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id integer primary key autoincrement,
        first_name text,
        last_name text,
        birth_date date,
        birth_place text);
""")

# Insert fake authors in table
cursor.executemany("INSERT INTO authors VALUES (NULL,?,?,?,?)", authors)

# Create books table in database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id integer primary key autoincrement,
        title text,
        genre text,
        num_pages integer,
        publish_year integer,
        author_id integer,
        FOREIGN KEY(author_id) REFERENCES authors(id) ON DELETE CASCADE );
    """)

# Fetching authors with their id and date of birth
fetch_authors = cursor.execute("SELECT id, birth_date FROM authors").fetchall()
author_birthdates = {row[0]: row[1] for row in fetch_authors}

# Generate books with faker module based on author ids and birthdays
books = []
for _ in range(1000):
    # Generate author ids in list and choose randomly from list
    author_id = random.choice(list(author_birthdates.keys()))
    author_birthdate = author_birthdates[author_id]

    # Extract year from author's birthdate
    birth_year = int(author_birthdate.split('-')[0])

    # Generate a publish year that is after the author's birth year
    publish_year = random.randint(birth_year + min_age, 2024)

    # Generate other book details
    book = (
        fake.sentence(nb_words=2).rstrip("."),  # Title
        random.choice(genres),  # Genre
        random.randint(20, 500),  # Number of pages
        publish_year,  # Publish year
        author_id  # Author ID (foreign key)
    )

    books.append(book)
# Insert books in table
cursor.executemany("INSERT INTO books VALUES (NULL,?,?,?,?,?)", books)

# Commit and close connection
conn.commit()
conn.close()