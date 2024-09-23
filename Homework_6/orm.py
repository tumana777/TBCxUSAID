from faker import Faker
import random
from datetime import datetime
from sqlalchemy import func
from models import session, Author, Book, author_book_association

# Initialize Faker
fake = Faker()

# Define genres
genres = [
    "Fantasy", "Science Fiction", "Mystery", "Thriller", "Romance", "Historical Fiction", "Horror",
    "Young Adult (YA)", "Dystopian", "Adventure", "Literary Fiction", "Non-Fiction",
    "Biography/Autobiography", "Self-Help", "Philosophical Fiction", "Poetry", "Magical Realism",
    "Crime", "Urban Fantasy", "Epic Fantasy", "Political Fiction", "Psychological Thriller", "Western",
    "Chick Lit", "Graphic Novel", "Paranormal Romance", "Suspense", "Legal Thriller", "Satire", "Travel"
]

min_age = 12
current_year = datetime.now().year

# Generate fake authors
authors = [
    Author(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        birth_date=fake.date_of_birth(minimum_age=min_age),
        birth_place=fake.country()
    ) for _ in range(500)
]

# Add authors to the session
session.add_all(authors)
session.commit()

# Refetch authors to ensure they're attached to the session
authors = session.query(Author).all()

# Fetching authors with their id and date of birth
author_birthdates = {
    author.id: author.birth_date for author in authors
}

# Generate books and assign random authors (1 to 3 authors per book)
books = []
for _ in range(1000):
    selected_authors = random.sample(authors, k=random.randint(1, 3))
    birth_year = min([author_birthdates[author.id].year for author in selected_authors])
    publish_year = random.randint(birth_year + min_age, current_year)

    book = Book(
        title=fake.sentence(nb_words=2).rstrip("."),
        genre=random.choice(genres),
        num_pages=random.randint(20, 500),
        publish_year=publish_year
    )

    # Assign authors to the book
    book.authors.extend(selected_authors)

    books.append(book)

# Add books to the session
session.add_all(books)
session.commit()

# Fetch and print books with the most pages
max_num_pages_subquery = session.query(func.max(Book.num_pages)).scalar_subquery()
max_pages_books = session.query(Book).filter(Book.num_pages == max_num_pages_subquery).all()

print("Here are the books with the most pages:")
for book in max_pages_books:
    authors_names = ', '.join([f"{author.first_name} {author.last_name}" for author in book.authors])
    print({
        "Book_id": book.id,
        "Title": book.title,
        "Genre": book.genre,
        "Num_pages": book.num_pages,
        "Publish_year": book.publish_year,
        "Authors": authors_names
    })

# Fetch and print the average number of pages of all books
average_pages = session.query(func.avg(Book.num_pages)).scalar()
print(f"\nAll the books pages average is {average_pages:.2f}")

# Fetch and print the youngest author
youngest_author = session.query(Author).order_by(Author.birth_date.desc()).first()
print(
    f"\nThe youngest author is '{youngest_author.first_name} {youngest_author.last_name}' born on '{youngest_author.birth_date}'")

# Fetch and print authors without books
authors_without_books = session.query(Author).outerjoin(author_book_association).filter(
    author_book_association.c.book_id == None).all()
print("\nHere are the authors that have no books yet:")
for author in authors_without_books:
    print({
        "Author_id": author.id,
        "Name": author.first_name + " " + author.last_name
    })

# Fetch and print 5 authors who have more than 3 books
authors_with_more_than_3_books = session.query(Author,
                                               func.count(author_book_association.c.book_id).label('book_count')).join(
    author_book_association).group_by(Author).having(func.count(author_book_association.c.book_id) > 3).limit(5).all()

print("\nHere are the 5 authors who have more than 3 books:")
for author, book_count in authors_with_more_than_3_books:
    print({
        "Author_id": author.id,
        "Name": author.first_name + " " + author.last_name,
        "Number_of_books": book_count
    })

# Close the session
session.close()
